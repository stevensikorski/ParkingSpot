"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  twilio.py
  Text notifications sent via SMS using Twilio.

"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER = os.getenv('RECIPIENT_PHONE_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

try:
  message = client.messages.create(
    body="This is just a test message.",
    from_=TWILIO_PHONE_NUMBER,
    to=RECIPIENT_PHONE_NUMBER
  )
  print(message.sid)
except Exception as error:
  print(error)