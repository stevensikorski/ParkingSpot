"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  endpoints.py
  File Description

"""

from fastapi import FastAPI
from fastapi.responses import Response, StreamingResponse
from starlette.background import BackgroundTask
from src.camera.picam import get_image_data, start_stream
from src.ml.model import generate_frames

app = FastAPI()

@app.get("/image")
def get_image():
    data = get_image_data()
    return Response(content=data, media_type="image/jpeg")

@app.get("/video")
async def get_video():
    picam2, output = start_stream()
    def stop():
        picam2.stop_recording()
        picam2.close()
    return StreamingResponse(
        generate_frames(output),
        media_type="multipart/x-mixed-replace; boundary=frame",
        background=BackgroundTask(stop),
    )