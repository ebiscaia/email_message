import json
import smtplib
import random

from email.message import EmailMessage

PHRASE_FILE = "phrases.txt"
AUTH_FILE = "auth.json"

with open(PHRASE_FILE) as f:
    lines = f.read().splitlines()

with open(AUTH_FILE) as af:
    auth = json.load(af)

# try sending an email
msg = EmailMessage()
msg["Subject"] = "Test Email"
msg["From"] = auth["email"]
msg["To"] = auth["to"]
msg.set_content("This is a test email sent via Python.")

# Associate the lines of the PHRASE_FILE to variables of languages and phrases
languages = lines[0].split("|")
phrases = lines[1:]

# Get a random phrase and separate the original part and its translation
phrase = phrases[random.randint(0, len(phrases) - 1)].split("|")

# Send the email securely (works with iCloud and Gmail):
with smtplib.SMTP(auth["outgoing_server"], auth["outgoing_port"]) as server:
    server.starttls()
    server.login(auth["email"], auth["password"])
    server.send_message(msg)
