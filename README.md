## ParkingSpot

ParkingSpot is a parking spot detection project designed to help find available street parking near my home. With only street parking available, I oftentimes have to circle my neighborhood looking for a space. This project is a practical solution allowing me to park my car in an ideal spot as soon as its made available, making street parking more manageable and convenient.

### Hardware Requirements

* Raspberry Pi 5 (8GB)
* Raspberry Pi M.2 HAT + HAILO AI Module (13 TOPS)
* Raspberry Pi Camera Module 3 (12MP)
* Additional components required for seamless integration

### Environment Setup

Copy the environment file and fill in required keys.
```
cp .env.example .env
```

### Instructions

```
Compile:

make clean
make all
```

```
Execute:

make run
```

### References

Camlytics. "Parking Spot Detection AI - Camlytics Camera Software." YouTube, 26 Sep. 2021, https://www.youtube.com/watch?v=U3gn663fniQ.

Ultralytics. YOLO Documentation. Ultralytics, https://docs.ultralytics.com.

OpenCV. "OpenCV: Python Tutorials." OpenCV Documentation, OpenCV, https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html. 

Pi-Cam. PiCourse, https://www.picourse.dev/pi-cam.