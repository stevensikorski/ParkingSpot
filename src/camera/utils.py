"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  utils.py
  Project utility functions.

"""

import cv2
import numpy as np

def enhance_low_light(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  avg_brightness = np.mean(gray)

  if avg_brightness < 50:
    brightness_factor = 1.2
    img = cv2.convertScaleAbs(img, alpha=brightness_factor, beta=20)

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    enhanced_lab = cv2.merge((l, a, b))
    img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

  return img