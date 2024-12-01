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
}

PARKING_SPOTS = [
  ((310, 1320), (500, 300)),
  ((1685, 1135), (500, 300)),
  ((3350, 1000), (300, 200)),
  ((2865, 985), (300, 200)),
  ((2275, 975), (200, 125)),
  ((2000, 950), (200, 125))
]

CENSOR_REGIONS = [
  ((2625, 250), (325, 200)),
  ((665, 580), (250, 150)),
  ((2205, 805), (80, 60)),
  ((985, 800), (60, 40))
]