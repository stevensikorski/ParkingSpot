# ParkingSpot

ssh stevensikorski@raspberrypi.local
python3 -m venv --system-site-packages venv
source venv/bin/activate
code ~/.gitignore_global
git config --get core.excludesfile

source venv/bin/activate
fastapi dev --host 0.0.0.0 main.py