"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  picam.py
  Handle image capture and video streaming.

"""

import io
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FileOutput
from threading import Condition
from src.app.constants import SETTINGS

def capture_image():
  picam2 = Picamera2()
  capture_config = picam2.create_still_configuration(main={"size": SETTINGS["RESOLUTION"]})
  picam2.configure(capture_config)
  data = io.BytesIO()
  picam2.start()
  picam2.capture_file(data, format="jpeg")
  picam2.stop()
  picam2.close()
  return data.getvalue()

def stream_video():
  picam2 = Picamera2()
  video_config = picam2.create_video_configuration(main={"size": SETTINGS["RESOLUTION"]})
  picam2.configure(video_config)
  output = MPJPEGStreamingOutput()
  picam2.start_recording(MJPEGEncoder(), FileOutput(output), Quality.VERY_HIGH)
  return picam2, output

class MPJPEGStreamingOutput(io.BufferedIOBase):
  def __init__(self):
    self.frame = None
    self.condition = Condition()

  def write(self, buf):
    with self.condition:
      self.frame = buf
      self.condition.notify_all()

  def read(self):
    with self.condition:
      self.condition.wait()
      return self.frame