from ultralytics import YOLO
import os

# 1. Load your best model
model = YOLO('bestf.pt')

# 2. Path to the image you want to check
image_path = r'c:user/adhee/downloads/test/images/LP_004680_png.rf.f588885fe6994a52ba65939257599ee5.jpg'
# We use a 0.5 confidence threshold to be balanced
results = model.predict(source=image_path, save=True, conf=0.5, show=True)

# 4. Logic to determine if it is a pipe or a target
for result in results:
    # If no boxes are found, it means it is a Normal Pipe (No detection)
    if len(result.boxes) == 0:
        print("\n" + "-"*40)
        print("Status: No unauthorized connections detected.")
        print("-"*40 + "\n")
    
    # If boxes ARE found, it means an LP feature was detected
    else:
        conf = result.boxes.conf[0].item()
        print("\n" + "!"*40)
        print("FINAL RESULT: TARGET DETECTED (LP)")
        print(f"Status: Unauthorized connection found with {conf:.2%} confidence.")
        print("!"*40 + "\n")