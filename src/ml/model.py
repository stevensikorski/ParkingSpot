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
from src.app.constants import SETTINGS, PARKING_SPOTS, CENSOR_REGIONS
from camera.utils import enhance_image
from src.app.utils import format_duration

spot_counters = {idx: 0 for idx in range(len(PARKING_SPOTS))}

async def generate_frames(output):
  model = YOLO("yolov8n_ncnn_model")
  logging.getLogger("ultralytics").setLevel(logging.WARNING)
  while True:
    try:
      jpeg_data = output.read()

      np_arr = np.frombuffer(jpeg_data, np.uint8)
      img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

      img = enhance_image(img)

      results = model(img)
      annotated_frame = annotate_image(results, img)

      _, annotated_frame_jpeg = cv2.imencode('.jpg', annotated_frame)
      yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + annotated_frame_jpeg.tobytes() + b"\r\n")
      await asyncio.sleep(SETTINGS["POLLING"])

    except Exception as e:
      logging.error(f"Error in generate_frames: {str(e)}")
      break

def annotate_image(results, img):
    overlay = img.copy()
    cars_in_spots = check_parking_spots(results, PARKING_SPOTS)

    for idx, ((x, y), (w, h)) in enumerate(PARKING_SPOTS):
      is_occupied = idx in cars_in_spots

      if not is_occupied:
        spot_counters[idx] += 1
      else:
        spot_counters[idx] = 0 

      if spot_counters[idx] == SETTINGS["TIME"]:
        print(f"NOTIFY: Spot {idx + 1} is available.")

      color = (0, 255, 0) if not is_occupied else (0, 0, 255)
      cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
      cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

      spot_id_text = f"Spot {idx + 1}"
      text_x = x + w // 2
      text_y = y + h // 2
      font_scale = 1
      font_thickness = 3
      text_size = cv2.getTextSize(spot_id_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]

      bg_color = color
      bg_x1 = text_x - text_size[0] // 2 - 5
      bg_y1 = text_y - text_size[1] // 2 - 5
      bg_x2 = text_x + text_size[0] // 2 + 5
      bg_y2 = text_y + text_size[1] // 2 + 5
      cv2.rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), bg_color, -1)

      text_color = (255, 255, 255)
      cv2.putText(img, spot_id_text, (text_x - text_size[0] // 2, text_y + text_size[1] // 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)

    alpha = 0.25
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # img = results[0].plot()
    
    boxes = results[0].boxes
    class_names = results[0].names
    for box in boxes:
      cls = int(box.cls)
      if class_names[cls] == "car":
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.circle(img, (center_x, center_y), 5, (255, 255, 255), -1)

    draw_parking_status(img, spot_counters)

    print(f"Cars detected in spots: {len(cars_in_spots)}")
    print(f"Available spots: {max(0, len(PARKING_SPOTS) - len(cars_in_spots))}")
    print(spot_counters)

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
        
def draw_parking_status(img, spot_counters):
  x_offset = 32
  y_offset = 32
  font_scale = 1
  font_thickness = 3
  box_padding = 10
  text_color = (255, 255, 255)

  for idx, counter in spot_counters.items():
    is_available = counter >= SETTINGS["TIME"]
    status_text = f"Spot {idx + 1}: {'Available' if is_available else 'Occupied'}"

    if is_available:
      duration_text = f" [{format_duration(counter)}]"
      status_text += duration_text

    bg_color = (0, 255, 0) if is_available else (0, 0, 255)

    text_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]

    bg_x1, bg_y1 = x_offset, y_offset
    bg_x2, bg_y2 = bg_x1 + text_size[0] + 2 * box_padding, bg_y1 + text_size[1] + 2 * box_padding
    cv2.rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), bg_color, -1)

    text_x = bg_x1 + box_padding
    text_y = bg_y1 + text_size[1] + box_padding
    cv2.putText(img, status_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)

    y_offset += text_size[1] + 2 * box_padding