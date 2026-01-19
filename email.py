FILE_NAME = "phrases.txt"

with open(FILE_NAME) as f:
    lines = f.read().splitlines()

print(len(lines))
