"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  picam.py
  File Description

"""

import io
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FileOutput
from threading import Condition

def get_image_data():
    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration(main={"size": (4608, 2598)})
    picam2.configure(capture_config)
    data = io.BytesIO()
    picam2.start()
    picam2.capture_file(data, format="jpeg")
    picam2.stop()
    picam2.close()
    return data.getvalue()

def start_stream():
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (4608, 2598)})
    picam2.configure(video_config)
    output = StreamingOutput()
    picam2.start_recording(MJPEGEncoder(), FileOutput(output), Quality.VERY_HIGH)
    return picam2, output

class StreamingOutput(io.BufferedIOBase):
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