.PHONY:

setup:
	python3 -m venv --system-site-packages venv
	@echo "Virtual environment created."

install:
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Dependencies installed."

test:
	. venv/bin/activate && python3 -m unittest discover
	@echo "All tests verified."

clean:
	rm -rf __pycache__ src/__pycache__
	rm -rf venv
	rm -rf yolov8n_ncnn_model
	rm -rf yolov8n.pt
	rm -rf yolov8n.torchscript
	@echo "Project files cleaned."

model:
	. venv/bin/activate && python3 src/convert.py
	@echo "Model conversion complete."

run:
	. venv/bin/activate && python3 -m fastapi dev --host 0.0.0.0 src/main.py
	@echo "Application started."

all: setup install model
