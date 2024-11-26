import io
import asyncio

from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FileOutput

from fastapi import FastAPI
from starlette.background import BackgroundTask
from fastapi.responses import Response
from fastapi.responses import StreamingResponse
from threading import Condition
import logging
from contextlib import asynccontextmanager
from ultralytics import YOLO
import numpy as np
import cv2


app = FastAPI()

@app.get("/image")
def get_image():
    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration(main={"size": (4608, 2598)})
    picam2.configure(capture_config)
    data = io.BytesIO()
    picam2.start()
    picam2.capture_file(data, format="jpeg")
    picam2.stop()
    picam2.close()
    return Response(content=data.getvalue(), media_type="image/jpeg")


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

async def generate_frames(output):
    model = YOLO("yolov8n_ncnn_model")
    while True:
        try:
            jpeg_data = output.read()

            # Convert jpeg data to an OpenCV image
            np_arr = np.frombuffer(jpeg_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Detect low-light conditions
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray)

            if avg_brightness < 50:  # Threshold for low light; adjust as needed
                # Enhance image for nighttime
                # Convert to LAB color space
                lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) on L channel
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                l = clahe.apply(l)
                enhanced_lab = cv2.merge((l, a, b))
                img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

                # Apply gamma correction
                gamma = 1.5  # Adjust gamma for brighter images
                gamma_correction = np.array([((i / 255.0) ** (1.0 / gamma)) * 255
                                             for i in np.arange(0, 256)]).astype("uint8")
                img = cv2.LUT(img, gamma_correction)

            # Get YOLO predictions
            results = model(img)
            boxes = results[0].boxes  # Get bounding boxes

            centers = []
            for box in boxes.xyxy:  # Iterate over bounding boxes
                x1, y1, x2, y2 = box[:4]  # Extract box coordinates
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                centers.append((center_x, center_y))

            # Annotate image with bounding boxes and centers
            annotated_frame = results[0].plot()
            for center_x, center_y in centers:
                cv2.circle(annotated_frame, (int(center_x), int(center_y)), 5, (0, 255, 0), -1)

            # Censor region example
            censor_region = (3150, 300, 375, 200)
            x, y, w, h = censor_region
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 0, 0), -1)

            censor_region = (800, 700, 250, 150)
            x, y, w, h = censor_region
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 0, 0), -1)

            # Encode the frame and yield it
            _, annotated_frame_jpeg = cv2.imencode('.jpg', annotated_frame)
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + annotated_frame_jpeg.tobytes() + b"\r\n")
            await asyncio.sleep(1)

        except Exception as e:
            logging.error(f"Error in generate_frames: {str(e)}")
            break

@app.get("/mjpeg")
async def mjpeg():
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (4608, 2598)})
    picam2.configure(video_config)
    output = StreamingOutput()
    picam2.start_recording(MJPEGEncoder(), FileOutput(output), Quality.VERY_HIGH)
    def stop():
        print("Stopping recording")
        picam2.stop_recording()
        picam2.close()
    return StreamingResponse(
        generate_frames(output),
        media_type="multipart/x-mixed-replace; boundary=frame",
        background=BackgroundTask(stop),
    )