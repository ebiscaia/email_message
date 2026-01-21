PHRASE_FILE = "phrases.txt"

with open(PHRASE_FILE) as f:
    lines = f.read().splitlines()

print(len(lines))
