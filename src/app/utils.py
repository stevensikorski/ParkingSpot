"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  utils.py
  Utility functions used across application.

"""

def format_duration(seconds):
  if seconds < 60:
    return f"{int(seconds)}s"
  elif seconds < 3600:
    return f"{int(seconds // 60)}m"
  else:
    return f"{int(seconds // 3600)}h"