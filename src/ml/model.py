"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  model.py
  File Description

"""

from ultralytics import YOLO
import numpy as np
import cv2
import asyncio
import logging

async def generate_frames(output):
    model = YOLO("yolov8n_ncnn_model")
    while True:
        try:
            jpeg_data = output.read()

            np_arr = np.frombuffer(jpeg_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            img = enhance_image(img)

            results = model(img)
            annotated_frame = annotate_image(results, img)

            _, annotated_frame_jpeg = cv2.imencode('.jpg', annotated_frame)
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" +
                   annotated_frame_jpeg.tobytes() + b"\r\n")
            await asyncio.sleep(1)

        except Exception as e:
            logging.error(f"Error in generate_frames: {str(e)}")
            break

def enhance_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    if avg_brightness < 50:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced_lab = cv2.merge((l, a, b))
        img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        gamma = 1.5
        gamma_correction = np.array(
            [((i / 255.0) ** (1.0 / gamma)) * 255 for i in np.arange(0, 256)]
        ).astype("uint8")
        img = cv2.LUT(img, gamma_correction)
    return img

def annotate_image(results, img):
    boxes = results[0].boxes
    annotated_frame = results[0].plot()
    for box in boxes.xyxy:
        x1, y1, x2, y2 = box[:4]
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        cv2.circle(annotated_frame, (int(center_x), int(center_y)), 5, (0, 255, 0), -1)
    return annotated_frame