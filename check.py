from ultralytics import YOLO

# Load trained model
model = YOLO("runs/detect/train10/weights/best.pt")

# Validate model
metrics = model.val(data="pipe.yaml")
