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
  "TIME": 5,
  "GAMMA": 1.5,
  "THRESHOLD": 50,
  "SCALE": 1,
  "THICKNESS": 3,
  "PADDING": 5,
  "OFFSET": 32,
  "CIRCLE": 5,
  "TEXT_COLOR": (255, 255, 255),
  "OCCUPIED_COLOR": (0, 0, 255),
  "AVAILABLE_COLOR": (0, 255, 0),
  "ALPHA": 0.25,
}

PARKING_SPOTS = [
  # ((x, y), (w, h))
  ((310, 1400), (500, 300)),
  ((1700, 1300), (500, 300)),
  ((3300, 1250), (300, 200)),
  ((2750, 1225), (300, 200)),
]

CENSOR_REGIONS = [
  # ((x, y), (w, h))
  ((2625, 475), (325, 200)),
  ((665, 700), (250, 150)),
  ((2215, 1040), (60, 40)),
  ((990, 960), (60, 40)),
]