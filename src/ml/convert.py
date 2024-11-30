"""

  Steven Sikorski
  CSCI49369 Computational Vision
  Final Project
  11/26/2024

  convert.py
  Exports the YOLOv8 model to NCNN format for efficient operation on device.

"""

from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.export(format="ncnn")