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
from src.app.spots import PARKING_SPOTS
from src.app.censor import CENSOR_REGIONS

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
    overlay = img.copy()

    for (x, y), (w, h) in PARKING_SPOTS:
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), -1)

    alpha = 0.25
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    for (x, y), (w, h) in PARKING_SPOTS:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    
    boxes = results[0].boxes
    class_names = results[0].names
    for box in boxes:
        cls = int(box.cls)
        if class_names[cls] == "car":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), -1)

    cars_in_spots = check_parking_spots(results, PARKING_SPOTS)
    print(f"Cars detected in spots: {len(cars_in_spots)}")
    print(f"Available spots: {len(PARKING_SPOTS) - len(cars_in_spots)}")

    for (x, y), (w, h) in CENSOR_REGIONS:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
    return img

def is_center_in_spot(center_x, center_y, spot):
  (x1, y1), (w, h) = spot
  x2 = x1 + w
  y2 = y1 + h
  return x1 <= center_x <= x2 and y1 <= center_y <= y2

def check_parking_spots(results, spots):
  parked_cars = []
  boxes = results[0].boxes
  class_names = results[0].names

  for box in boxes:
        cls = int(box.cls)
        if class_names[cls] == "car":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            for idx, spot in enumerate(spots):
                if is_center_in_spot(center_x, center_y, spot):
                    parked_cars.append(idx)
                    break
  return parked_cars

async def track_parking(picam2, output):
    model = YOLO("yolov8n_ncnn_model")
    while True:
        try:
            jpeg_data = output.read()

            np_arr = np.frombuffer(jpeg_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            img = enhance_image(img)

            results = model(img)

            cars_in_spots = check_parking_spots(results, PARKING_SPOTS)
            available_spaces = len(PARKING_SPOTS) - len(cars_in_spots)

            yield {
                "available_spaces": available_spaces,
                "total_spots": len(PARKING_SPOTS)
            }

            await asyncio.sleep(1)

        except Exception as e:
            logging.error(f"Error in track_parking: {str(e)}")
            break