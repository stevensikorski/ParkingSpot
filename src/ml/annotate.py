"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  annotate.py
  Annotating the MJPEG image stream.

"""

import cv2
from src.app.constants import SETTINGS, PARKING_SPOTS, CENSOR_REGIONS
from src.app.utils import format_duration
from src.ml.track import check_parking_spots
from src.notify.notify import SMSNotifier

def annotate_image(results, img, counter):
  cars_in_spots = check_parking_spots(results, PARKING_SPOTS)

  # img = results[0].plot()
  img = draw_parking_spots(img, cars_in_spots, counter)
  img = draw_car_boxes(results, img)
  img = apply_censorship(img)
  img = draw_parking_status(img, counter)

  print(f"Cars detected in spots: {len(cars_in_spots)}")
  print(f"Available spots: {max(0, len(PARKING_SPOTS) - len(cars_in_spots))}")
  print(counter)

  return img

def draw_parking_spots(img, cars_in_spots, counter):
  overlay = img.copy()

  for i, ((x, y), (w, h)) in enumerate(PARKING_SPOTS):
    is_occupied = i in cars_in_spots

    if not is_occupied:
      counter[i] += 1
    else:
      counter[i] = 0

    if counter[i] == SETTINGS["TIME"]:
      print(f"NOTIFY: Spot {i + 1} is available.")
      duration = format_duration(counter[i])
      SMSNotifier().send_notification(i, duration)

    color = SETTINGS["AVAILABLE_COLOR"] if not is_occupied else SETTINGS["OCCUPIED_COLOR"]
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

    spot_id_text = f"Spot {i + 1}"
    text_x = x + w // 2
    text_y = y + h // 2
    draw_text_with_background(img, spot_id_text, text_x, text_y, color)

  cv2.addWeighted(overlay, SETTINGS["ALPHA"], img, 1 - SETTINGS["ALPHA"], 0, img)
  return img

def draw_car_boxes(results, img):
  boxes = results[0].boxes
  class_names = results[0].names

  for box in boxes:
    cls = int(box.cls)
    if class_names[cls] == "car":
      x1, y1, x2, y2 = map(int, box.xyxy[0])
      center_x = (x1 + x2) // 2
      center_y = (y1 + y2) // 2
      cv2.rectangle(img, (x1, y1), (x2, y2), SETTINGS["TEXT_COLOR"], 2)
      cv2.circle(img, (center_x, center_y), SETTINGS["CIRCLE"], SETTINGS["TEXT_COLOR"], -1)

  return img

def apply_censorship(img):
  for (x, y), (w, h) in CENSOR_REGIONS:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
  return img

def draw_parking_status(img, counter):
  x_offset, y_offset = SETTINGS["OFFSET"], SETTINGS["OFFSET"]

  for i, count in counter.items():
    is_available = count >= SETTINGS["TIME"]
    status_text = f"Spot {i + 1}: {'Available' if is_available else 'Occupied'}"

    if is_available:
      duration_text = f" [{format_duration(count)}]"
      status_text += duration_text

    bg_color = SETTINGS["AVAILABLE_COLOR"] if is_available else SETTINGS["OCCUPIED_COLOR"]
    text_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, SETTINGS["SCALE"], SETTINGS["THICKNESS"])[0]

    bg_x1, bg_y1 = x_offset, y_offset
    bg_x2, bg_y2 = bg_x1 + text_size[0] + 2 * SETTINGS["PADDING"], bg_y1 + text_size[1] + 2 * SETTINGS["PADDING"]
    cv2.rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), bg_color, -1)

    text_x = bg_x1 + SETTINGS["PADDING"]
    text_y = bg_y1 + text_size[1] + SETTINGS["PADDING"]
    cv2.putText(img, status_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, SETTINGS["SCALE"], SETTINGS["TEXT_COLOR"], SETTINGS["THICKNESS"])

    y_offset += text_size[1] + 2 * SETTINGS["PADDING"]
  return img

def draw_text_with_background(img, text, x, y, color):
  text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, SETTINGS["SCALE"], SETTINGS["THICKNESS"])[0]

  bg_x1 = x - text_size[0] // 2 - 5
  bg_y1 = y - text_size[1] // 2 - 5
  bg_x2 = x + text_size[0] // 2 + 5
  bg_y2 = y + text_size[1] // 2 + 5
  cv2.rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), color, -1)
  cv2.putText(img, text, (x - text_size[0] // 2, y + text_size[1] // 2), cv2.FONT_HERSHEY_SIMPLEX, SETTINGS["SCALE"], SETTINGS["TEXT_COLOR"], SETTINGS["THICKNESS"])