from bnet import *

from collections import defaultdict

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
        denominator = counts[variables[:-1]][values[:-1]]
        numerator = counts[variables][values]
        probabilities[variables][values] = numerator / denominator if denominator > 0 else 0

# Print the conditional probability tables
for variable in ['B', 'G', 'C', 'F']:
    print(f'P({variable})')
    for value in [0, 1]:
        print(f'  P({variable}={value}) = {probabilities[variable][value]:.3f}')
    print()

for variables in [('B', 'G'), ('G', 'C'), ('C', 'F'), ('B', 'F', 'G')]:
    var_names = ', '.join(variables)
    print(f'P({var_names})')
    for values in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        value_names = ', '.join(map(str, values))
        print(f'  P({var_names}={value_names}) = {probabilities[variables][values]:.3f}')
    print()
