import sys

if len(sys.argv) != 2:
    print("Usage: python bnet.py <training_data>")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    data = []
    for line in f:
        observation = tuple(map(int, line.strip().split()))
        data.append(observation)

