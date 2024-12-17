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
TWILIO_FROM_PHONE = os.getenv('TWILIO_FROM_PHONE')
TWILIO_TO_PHONE = os.getenv('TWILIO_TO_PHONE')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

try:
  message = client.messages.create(
    body="This is just a test message.",
    from_=TWILIO_FROM_PHONE,
    to=TWILIO_TO_PHONE
  )
  print(message.sid)
except Exception as error:
  print(error)