import json

PHRASE_FILE = "phrases.txt"
AUTH_FILE = "auth.json"

with open(PHRASE_FILE) as f:
    lines = f.read().splitlines()

print(len(lines))
