import sys
from collections import defaultdict

# Parse command line arguments
training_data_filename = sys.argv[1]
B = sys.argv[2] == 'Bt'
G = sys.argv[3] == 'Gt'
C = sys.argv[4] == 'Ct'
F = sys.argv[5] == 'Ft'

# Load training data
data = []
with open(training_data_filename, 'r') as f:
    for line in f:
        b, g, c, f = [int(x) for x in line.strip().split()]
        data.append((b, g, c, f))

# Count the number of occurrences of each combination of variable values
counts = defaultdict(lambda: defaultdict(int))

for observation in data:
    b, g, c, f = observation
    counts['B'][b] += 1
    counts['G'][g] += 1
    counts['C'][c] += 1
    counts['F'][f] += 1
    counts[('B', 'G')][(b, g)] += 1
    counts[('G', 'C')][(g, c)] += 1
    counts[('C', 'F')][(c, f)] += 1
    counts[('B', 'F', 'G')][(b, f, g)] += 1

# Calculate the conditional probabilities
probabilities = defaultdict(lambda: defaultdict(float))

for variable in ['B', 'G', 'C', 'F']:
    for value in [0, 1]:
        probabilities[variable][value] = counts[variable][value] / len(data)

for variables in [('B', 'G'), ('G', 'C'), ('C', 'F'), ('B', 'F', 'G')]:
    for values in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        probabilities[variables][values] = counts[variables][values] / counts[variables[:-1]][values[:-1]]

# Calculate the joint probability of the given variable values
joint_probability = probabilities['B'][B] * probabilities['G'][G] * probabilities['C'][C] * probabilities['F'][F]
joint_probability /= probabilities[('B', 'G')][(B, G)]
joint_probability /= probabilities[('G', 'C')][(G, C)]
joint_probability /= probabilities[('C', 'F')][(C, F)]
joint_probability *= probabilities[('B', 'F', 'G')][(B, F, G)]

# Print the conditional probability tables and the calculated joint probability
print(f'P(B={B}, G={G}, C={C}, F={F}) = {joint_probability:.5f}')
