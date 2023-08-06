from collections import defaultdict
import sys

# Read command line arguments
training_file = sys.argv[1]
query_variables = {}
evidence_variables = {}

given = False
for i in range (2, len(sys.argv)):
    if sys.argv[i].lower() == "given":
        given = True
        continue
    if given:
        evidence_variables[sys.argv[i][0]] = int(sys.argv[i][1] == "t")
    else:
        query_variables[sys.argv[i][0]] = int(sys.argv[i][1] == "t")

print("B: Baseball Game on TV\nG: George watches TV\nC: George is out of Cat Food\nF: George feeds his cat\n")
# Load training data
data = []
with open(training_file, "r") as f:
    for line in f:
        data.append(tuple(map(int, line.strip().split())))

# Count the number of occurrences of each combination of variable values
counts = defaultdict(lambda: defaultdict(int))

for observation in data:
    b, g, c, f = observation
    counts['B'][b] += 1
    counts['G'][g] += 1
    counts['C'][c] += 1
    counts['F'][f] += 1
    counts[('B', 'G')][(b, g)] += 1
    counts[('G', 'F')][(g, f)] += 1
    counts[('C', 'F')][(c, f)] += 1
    counts[('G', 'F', 'C')][(g, f, c)] += 1

# Calculate the conditional probabilities
probabilities = defaultdict(lambda: defaultdict(float))

for variable in ['B', 'G', 'C', 'F']:
    for value in [0, 1]:
        probabilities[variable][value] = counts[variable][value] / len(data)

for variables in [('B', 'G'), ('G', 'C'), ('C', 'F'), ('B', 'F', 'G')]:
    for values in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        probabilities[variables][values] = counts[variables][values] / (counts[variables[:-1]][values[:-1]]+ 1e-9)

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
    joint_probability = enumerate_all(['B', 'G', 'C', 'F'], evidence_variables)
    evidence_probability = enumerate_all(evidence_variables.keys(), evidence_variables)
    if not query_variables:
        return joint_probability 
    else:
        query_probability = enumerate_all(query_variables.keys(), dict(evidence_variables, **query_variables))
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