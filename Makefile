.PHONY: all run clean

all:
	python3 -m venv --system-site-packages venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && python3 src/ml/convert.py

run:
	. venv/bin/activate && python3 -m fastapi dev --host 0.0.0.0 src/main.py

clean:
	rm -rf __pycache__ src/__pycache__ src/app/__pycache__ src/camera/__pycache__ src/ml/__pycache__ src/notify/__pycache__
	rm -rf venv
	rm -rf yolov8n_ncnn_model
	rm -rf yolov8n.pt
	rm -rf yolov8n.torchscript