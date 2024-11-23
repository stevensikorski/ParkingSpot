from setuptools import setup

setup(
  name="ParkingSpot",
  version="1.0.0",
  description="ParkingSpot simplifies street parking by leveraging computer vision and machine learning to detect and notify users of available parking spaces in real time.",
  install_requires=[
    "fastapi[standard]>=0.115.5",
    "numpy>=1.24.2",
    "opencv-python-headless>=4.10.0.84",
    "ultralytics>=8.3.34"
  ]
)