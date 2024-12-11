"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  constants.py
  Define constants utilized by application.

"""

SETTINGS = {
  "RESOLUTION": (3840, 2160),
  "POLLING": 1,
  "THRESHOLD": 30,
}

TEXT = {
  "SCALE": 1,
  "THICKNESS": 3,
  "PADDING": 10,
  "OFFSET": 32,
  "COLOR": (255, 255, 255)
}

BOX = {
  "OCCUPIED_COLOR": (0, 0, 255),
  "AVAILABLE_COLOR": (0, 255, 0),
  "ALPHA": 0.25
}

PARKING_SPOTS = [
  ((310, 1420), (500, 300)),
  ((1700, 1300), (500, 300)),
  ((3350, 1225), (300, 200)),
  ((2865, 1210), (300, 200)),
  # ((2325, 1150), (200, 125)),
  # ((2075, 1135), (200, 125))
  ((3540, 1860), (300, 300)),
]

CENSOR_REGIONS = [
  ((2625, 450), (325, 200)),
  ((665, 700), (250, 150)),
  ((2205, 1005), (60, 40)),
  ((985, 800), (60, 40))
]