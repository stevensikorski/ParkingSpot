"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  track.py
  Parking tracking utilities.

"""

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