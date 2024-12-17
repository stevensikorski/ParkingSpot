"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  notify.py
  Parking spot notifications sent via SMS.

"""

import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class SMSNotifier:
  def __init__(self):
    self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    self.from_phone = os.getenv("TWILIO_FROM_PHONE")
    self.to_phone = os.getenv("TWILIO_TO_PHONE")
    self.client = Client(self.account_sid, self.auth_token)

  def send_notification(self, spot_id, duration):
    try:
      text = f"Spot {spot_id + 1} has become available."
      message = self.client.messages.create(
        body=text,
        from_=self.from_phone,
        to=self.to_phone
      )
      print(f"Message: {message.sid}, Sent: {text}")
    except Exception as error:
      print(error)