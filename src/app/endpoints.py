"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  endpoints.py
  File Description

"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
from fastapi.responses import Response, StreamingResponse
from starlette.background import BackgroundTask
from src.camera.picam import capture_image, stream_video
from src.ml.model import generate_frames
from src.app.constants import PARKING_SPOTS
from src.ml.model import check_parking_spots
from src.ml.model import track_parking

app = FastAPI()

@app.get("/image")
def get_image():
  data = capture_image()
  return Response(content=data, media_type="image/jpeg")

@app.get("/video")
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

@app.get("/")
async def get_json_data(output: BackgroundTasks):
  picam2, output = stream_video()

  def stop():
      picam2.stop_recording()
      picam2.close()

  try:
      async for data in track_parking(picam2, output):
          return JSONResponse(content=data)
  finally:
      stop()
