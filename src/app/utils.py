"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  utils.py
  Utility functions used across the application.

"""

import cv2
import numpy as np
from src.app.constants import SETTINGS

def enhance_image(image):
  gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  mean_brightness = np.mean(gray_scale)

  if mean_brightness > SETTINGS["THRESHOLD"]:
    return image

  gamma_value = SETTINGS["GAMMA"]
  inverse_gamma = 1.0 / gamma_value
  corrected_image = np.power(image / 255.0, inverse_gamma) * 255
  return corrected_image

def format_duration(seconds):
  if seconds < 60:
    return f"{int(seconds)}s"
  elif seconds < 3600:
    return f"{int(seconds // 60)}m"
  else:
    return f"{int(seconds // 3600)}h"