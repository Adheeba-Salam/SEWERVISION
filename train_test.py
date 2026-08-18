from ultralytics import YOLO

# Load the model
model = YOLO('yolo11s.pt') 

# Start training - this will take time!
model.train(data='pipe.yaml', epochs=100, imgsz=640, batch=8,device='Gpu')

print("Step 4: Training finished", flush=True)
