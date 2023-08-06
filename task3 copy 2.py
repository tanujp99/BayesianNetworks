from collections import defaultdict
import sys

# Read command line arguments
# training_file = sys.argv[1]
# query_variables = {}
# evidence_variables = {}

# given = False
# for i in range (2, len(sys.argv)):
#     if sys.argv[i].lower() == "given":
#         given = True
#         continue
#     if given:
#         evidence_variables[sys.argv[i][0]] = int(sys.argv[i][1] == "t")
#     else:
#         query_variables[sys.argv[i][0]] = int(sys.argv[i][1] == "t")

# Read command line arguments
training_file = "training_data.txt"
argvwer = ["Bt","Gt","Ct","Ft"]
query_variables = {}
evidence_variables = {}

given = False
for i in range ( len(argvwer)):
    if argvwer[i] == "given":
        given = True
        continue
    if given:
        evidence_variables[argvwer[i][0]] = int(argvwer[i][1] == "t")
    else:
        query_variables[argvwer[i][0]] = int(argvwer[i][1] == "t")

print("B: Baseball Game on TV\nG: George watches TV\nC: George is out of Cat Food\nF: George feeds his cat\n")
# Load training data
data = []
with open(training_file, "r") as f:
    for line in f:
        data.append(tuple(map(int, line.strip().split())))

# Count the number of occurrences of each combination of variable values
counts = defaultdict(lambda: defaultdict(int))
probabilities = {}

for observation in data:
    b, g, c, f = observation
    counts['B'][b] += 1
    counts['G'][g] += 1
    counts['C'][c] += 1
    counts['F'][f] += 1
    counts[('B', 'G')][(b, g)] += 1
    counts[('G', 'F')][(g, f)] += 1
    counts[('C', 'F')][(c, f)] += 1
    counts[('B', 'C', 'G')][(b, c, g)] += 1
    counts[('C', 'G', 'F')][(c, g, f)] += 1
    counts[('B', 'G', 'F')][(b, g, f)] += 1
    counts[('B', 'C', 'G', 'F')][(b, c, g, f)] += 1

# Calculate the conditional probabilities
probabilities = {}

for variable in ['B', 'G', 'C', 'F']:
    probabilities[variable] = {}
    for value in [0, 1]:
        probabilities[variable][value] = counts[variable][value] / len(data)

for variables in [('B', 'G'), ('G', 'F'), ('C', 'F')]:
    probabilities[variables] = {}
    for x in [0,1]:
        for y in [0,1]:
            probabilities[variables][(x,y)] = counts[variables][(x,y)] / len(data)
for variables in [ ('C', 'G', 'F'),('B', 'C', 'G'),('B', 'G', 'F')]:
    probabilities[variables] = {}
    for x in [0,1]:
        for y in [0,1]:
            for z in [0,1]:
                probabilities[variables][(x,y,z)] = counts[variables][(x,y,z)] / len(data)
for variables in [ ('B', 'C', 'G', 'F')]:
    probabilities[variables] = {}
    for x in [0,1]:
        for y in [0,1]:
            for z in [0,1]:
                for t in [0,1]:
                    probabilities[variables][(x,y,z,t)] = counts[variables][(x,y,z,t)] / len(data)
print(probabilities)

# Define function to perform inference by enumeration
def enumerate_all(variables, evidence):
    variables = list(variables)  # Convert to list before using it
    if not variables:
        return 1.0
    Y = variables[0]
    if Y in evidence:
        return probabilities[Y][evidence[Y]] * enumerate_all(variables[1:], evidence)
    else:
        return sum(probabilities[Y][y] * enumerate_all(variables[1:], dict(evidence, **{Y: y})) for y in [0, 1])

# Define function to calculate conditional probabilities using inference by enumeration
def calculate_conditional_probability(query_variables, evidence_variables):
    evidence_probability = enumerate_all(evidence_variables.keys(), evidence_variables)
    if not evidence_variables:
        return enumerate_all(['B', 'G', 'C', 'F'], query_variables) 
    else:
        query_probability = enumerate_all(list(query_variables.keys()) + list(evidence_variables.keys()), dict(query_variables, **evidence_variables))
        return query_probability / (evidence_probability + 1e-9)

# Perform inference by enumeration
if evidence_variables:
    probability = calculate_conditional_probability(query_variables, evidence_variables)
else:
    probability = calculate_conditional_probability(query_variables, {})

# Print the probability
if query_variables:
    query_string = ", ".join([f"{variable}={bool(value)}" for variable, value in query_variables.items()])
    evidence_string = ", ".join([f"{variable}={bool(value)}" for variable, value in evidence_variables.items()])
    print(f"P({query_string}{' | ' if given else ''}{evidence_string}) = {probability}\n")