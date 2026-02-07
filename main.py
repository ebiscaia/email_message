import json
import smtplib
import random
import logging

from email.message import EmailMessage

# Setting the logging system up
logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime}:{levelname}: {message}",
    style="{",
    datefmt="%d/%m/%Y %H:%M",
)

PHRASE_FILE = "phrases.txt"
AUTH_FILE = "auth.json"
message = ""

try:
    with open(AUTH_FILE) as af:
        auth = json.load(af)

    logging.debug(f"File {AUTH_FILE} read.")

    with open(PHRASE_FILE) as f:
        lines = f.read().splitlines()

    logging.debug(f"File {PHRASE_FILE} read.")

    # Associate the lines of the PHRASE_FILE to variables of languages and phrases
    languages = lines[0].split("|")
    phrases = lines[1:]

    # Check whether there are any phrases to be sent
    if not phrases:
        print("There are no phrases to be sent. Stopping program.")
        exit(1)

    # Get a random phrase and separate the original part and its translation
    index = random.randint(0, len(phrases) - 1)
    phrase = phrases[index].split("|")

    # Build the message
    message = f"""Phrase of the day
    {languages[0]}: {phrase[0]}
    {languages[1]}: {phrase[1]}"""

    # Check the lenght of phrases array and add a warning to the main message
    if len(phrases) == 1:
        message += """

    This is the last phrase of the file. Generate a new version of the file,
    otherwise this program will fail next time.
    """

    # try sending an email
    msg = EmailMessage()
    msg["Subject"] = "Test Email"
    msg["From"] = auth["email"]
    msg["To"] = auth["to"]
    msg.set_content(message)

    # Send the email securely (works with iCloud and Gmail):
    with smtplib.SMTP(auth["outgoing_server"], auth["outgoing_port"]) as server:
        server.starttls()
        server.login(auth["email"], auth["password"])
        server.send_message(msg)
    # Update lines array without the sent phrase (index+1 because of header)
    lines.pop(index + 1)
    linesString = "\n".join(lines)

    # Overwrite the file
    with open("phrases.txt", "w") as f:
        f.write(linesString)
except Exception as e:
    logging.error(f"Error: {e}.")
