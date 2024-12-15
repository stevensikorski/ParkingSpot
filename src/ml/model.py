"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  model.py
  Model processing for MJPEG image stream.

"""

from ultralytics import YOLO
import numpy as np
import cv2
import asyncio
import logging

from src.app.constants import SETTINGS, PARKING_SPOTS
from src.app.utils import enhance_image
from src.ml.annotate import annotate_image

class ParkingSpot:
  def __init__(self):
    self.model = YOLO("yolov8n_ncnn_model")
    self.counter = {idx: 0 for idx in range(len(PARKING_SPOTS))}
    logging.getLogger("ultralytics").setLevel(logging.WARNING)

  async def generate_frames(self, output):
    while True:
      try:
        jpeg_data = output.read()

        np_arr = np.frombuffer(jpeg_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        img = enhance_image(img)
        results = self.model(img)
        annotated_frame = annotate_image(results, img, self.counter)

        _, annotated_frame_jpeg = cv2.imencode('.jpg', annotated_frame)
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + annotated_frame_jpeg.tobytes() + b"\r\n")
        await asyncio.sleep(SETTINGS["POLLING"])

      except Exception as e:
        logging.error(f"Error in generate_frames: {str(e)}")
        break