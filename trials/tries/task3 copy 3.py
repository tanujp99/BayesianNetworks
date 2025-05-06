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
probabilities = {}

for observation in data:
    b, g, c, f = observation
    counts['B'][b] += 1
    counts['G'][g] += 1
    counts['C'][c] += 1
    counts['F'][f] += 1
    counts[('B', 'G')][(b, g)] += 1
    counts[('F', 'G')][(f, g)] += 1
    counts[('C', 'F')][(c, f)] += 1
    counts[('B', 'C', 'G')][(b, c, g)] += 1
    counts[('C', 'F', 'G')][(c, f, g)] += 1
    counts[('B', 'F', 'G')][(b, f, g)] += 1
    counts[('B', 'C', 'F', 'G')][(b, c, f, g)] += 1

# Calculate the conditional probabilities
probabilities = {}
for variable in ['B', 'G', 'C', 'F']:
    probabilities[variable] = {}
    for value in [0, 1]:
        probabilities[variable][value] = counts[variable][value] / len(data)
for variables in [('B', 'G'),('F', 'G'), ('C', 'F')]:
    probabilities[variables] = {}
    for x in [0,1]:
        for y in [0,1]:
            probabilities[variables][(x,y)] = counts[variables][(x,y)] / len(data)
for variables in [ ('C', 'F', 'G'),('B', 'C', 'G'),('B', 'F', 'G')]:
    probabilities[variables] = {}
    for x in [0,1]:
        for y in [0,1]:
            for z in [0,1]:
                probabilities[variables][(x,y,z)] = counts[variables][(x,y,z)] / len(data)
for variables in [ ('B', 'C', 'F', 'G')]:
    probabilities[variables] = {}
    for x in [0,1]:
        for y in [0,1]:
            for z in [0,1]:
                for t in [0,1]:
                    probabilities[variables][(x,y,z,t)] = counts[variables][(x,y,z,t)] / len(data)
# print(probabilities)

# Define function to perform inference by enumeration
def numcalc(queryl, query_variables,altset):
    num_calc = {'B':0, 'C':0, 'F':0, 'G':0}
    foo = 0
    
    for x in ['B', 'C', 'F', 'G']:
        if x in queryl:
            num_calc[x] = query_variables[x]  
        else:
            num_calc[x] = altset[foo]
            foo += 1
    print(num_calc)
    return num_calc


def enumerate(query_variables):
    queryl = tuple(query_variables.keys())

    probability = 0
    alternate = 4 - len(queryl)
    alts = {
    'alt4' : [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]],
    'alt3' : [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)],
    'alt2' : [[0, 0], [0, 1], [1, 0], [1, 1]],
    'alt1' : [[0],[1]],
    'alt0': [int] }
    altset = alts[f'alt{alternate}']
    for w in altset:
        num_calc = numcalc(queryl, query_variables, w)
        searchl = tuple(num_calc.keys())
        searchk = tuple(num_calc.values())
        probability += probabilities[searchl][searchk]
        # print(probability)
    print("----------------------",probability)
    return probability

# Define the function to calculate the conditional probabilities using inference by enumeration
def calculate_conditional_probability(query_variables, evidence_variables):
    numerator = {**query_variables, **evidence_variables}
    denominator = evidence_variables

    num_prob = enumerate(numerator)
    den_prob = enumerate(denominator)

    if not evidence_variables:
        ccd = num_prob
    else:
        ccd = (num_prob/den_prob)
    return ccd

# Perform inference by enumeration
if evidence_variables:
    probability = calculate_conditional_probability(query_variables, evidence_variables)
else:
    probability = calculate_conditional_probability(query_variables, {})

# Print the probability
query_string = ", ".join([f"{variable}={bool(value)}" for variable, value in query_variables.items()])
evidence_string = ", ".join([f"{variable}={bool(value)}" for variable, value in evidence_variables.items()])
print(f"\nP({query_string}{' | ' if given else ''}{evidence_string}) = {probability}\n")