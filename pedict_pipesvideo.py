from ultralytics import YOLO
import cv2

# 1. Load your best model
# Using the best weights from your successful train8 run
model = YOLO('best2.pt') 

# 2. Path to the video you want to check
# Replace this with the path to your sewer CCTV video
video_path = r'C:\Users\adhee\Downloads\WhatsApp Video 2026-02-15 at 9.51.05 AM.mp4'

# 3. Run the prediction on the video
# We use stream=True for videos to save memory
results = model.predict(source=video_path, save=True, conf=0.5, show=True, stream=True)

# 4. Loop through the video frames to process results
for result in results:
    # Logic to determine if a target is in the current frame
    if len(result.boxes) == 0:
        print("Status: No unauthorized connections detected.")
    else:
        # Extract confidence of the first detection
        conf_value = result.boxes.conf[0].item()
        print(f"Status: UNAUTHORIZED CONNECTION DETECTED! (Conf: {conf_value:.2f})")

    # Required to keep the display window active and allow 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()