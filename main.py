#!/usr/bin/python3

import json
import smtplib
import logging
import random

from email.message import EmailMessage
from logging.handlers import TimedRotatingFileHandler

# Define some of the main variables
PHRASE_FILE = "files/phrases.txt"
AUTH_FILE = "files/auth.json"
LOG_FILE = "files/app.log"
message = ""

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = TimedRotatingFileHandler(
    filename=LOG_FILE, when="W6", backupCount=10, encoding="utf-8"
)

# Create a console handler
console_handler = logging.StreamHandler()

# Set the handler formatter
formatter = logging.Formatter(
    datefmt="%d/%m/%Y %H:%M:%S",
    fmt="{name}:{asctime}:{levelname}: {message}",
    style="{",
)

# Set the formatter to the handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Main program
try:
    with open(AUTH_FILE) as af, open(PHRASE_FILE) as f:
        auth = json.load(af)
        lines = f.read().splitlines()

    for file in [AUTH_FILE, PHRASE_FILE]:
        logger.debug(f"File {file} read.")

    # Associate the lines of the PHRASE_FILE to variables of languages and phrases
    languages = lines[0].split("|")
    phrases = lines[1:]

    logger.debug(f"Language pair: {languages[0]}/{languages[1]}")

    # Check whether there are any phrases to be sent
    if not phrases:
        logger.error("There are no phrases to be sent. Stopping program.")
        exit(1)

    # Get a random phrase and separate the original part and its translation
    index = random.randint(0, len(phrases) - 1)
    phrase = phrases[index].split("|")

    # Build the message
    message = f"""
    {languages[0]}: {phrase[0]}
    {languages[1]}: {phrase[1]}"""

    # Check the lenght of phrases array and add a warning to the main message
    if len(phrases) == 1:
        message += """

    This is the last phrase of the file. Generate a new version of the file,
    otherwise this program will fail next time.
    """
        # Also log it
        logger.warning(
            "Last remaining phrase. Update the file to avoid an error next time the program is run."
        )
    else:
        logger.info(
            f"There is/are {len(phrases)-1} remaining phrase(s) in the file."
        )

    # try sending an email
    msg = EmailMessage()
    msg["Subject"] = "Phrase of the day"
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

    logger.debug(f'An email was sent to {auth["to"]} successfully.')
    # Overwrite the file
    with open(PHRASE_FILE, "w") as f:
        f.write(linesString)
    logger.debug(f"File {PHRASE_FILE} was saved successfully.")
except Exception as e:
    logger.error(f"Error: {e}.")
