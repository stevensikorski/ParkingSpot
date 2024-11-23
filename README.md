# ParkingSpot

ssh stevensikorski@raspberrypi.local
python3 -m venv --system-site-packages venv
source venv/bin/activate
code ~/.gitignore_global
git config --get core.excludesfile

source venv/bin/activate
fastapi dev --host 0.0.0.0 src/main.py
deactivate

http://raspberrypi.local:8000/mjpeg


python3 -m venv --system-site-packages venv
pip install .
python3 src/convert.py
fastapi dev --host 0.0.0.0 src/main.py