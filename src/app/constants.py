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
  "TIME": 30,
  "GAMMA": 2.0,
  "THRESHOLD": 50,
  "SCALE": 1,
  "THICKNESS": 3,
  "PADDING": 10,
  "OFFSET": 32,
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
  # ((2325, 1150), (200, 125)),
  # ((2075, 1135), (200, 125)),
  # ((3540, 1860), (300, 300)),
]

CENSOR_REGIONS = [
  # ((x, y), (w, h))
  ((2625, 475), (325, 200)),
  ((665, 700), (250, 150)),
  ((2205, 1045), (60, 40)),
  ((985, 950), (60, 40)),
]