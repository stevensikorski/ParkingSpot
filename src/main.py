"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  main.py
  Run ParkingSpot on a local server with endpoints.

"""

import uvicorn
from src.app.endpoints import app

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)