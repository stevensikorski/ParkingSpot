"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  convert.py
  File Description

"""

from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.export(format="ncnn", save_dir="src/models")
