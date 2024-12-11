"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  endpoints.py
  Endpoints for ParkingSpot API.

"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from src.camera.picam import stream_video
from src.ml.model import generate_frames

app = FastAPI()

@app.get("/")
async def get_video():
  picam2, output = stream_video()
  def stop():
    picam2.stop_recording()
    picam2.close()
  return StreamingResponse(
    generate_frames(output),
    media_type="multipart/x-mixed-replace; boundary=frame",
    background=BackgroundTask(stop),
  )