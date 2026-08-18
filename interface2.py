import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO
import threading
import cv2
import time
import requests
from datetime import datetime
import winsound  

# ================= TELEGRAM CONFIG =================
BOT_TOKEN="8764831417:AAE4Ui8KHcto3PIC7Rt5fhPyEl0gKQYHsaY"
CHAT_ID = "6420019030"

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

# ================= REPORT =================
def generate_report(status, count, confidence):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""
===== SEWER DETECTION REPORT =====
Time: {now}
Status: {status}
Pipes Detected: {count}
Highest Confidence: {confidence:.2f}
=================================
"""

    filename = f"report_{int(time.time())}.txt"
    with open(filename, "w") as f:
        f.write(report)

    print("Report saved:", filename)

# ================= YOLO =================
model = YOLO('bestf.pt')

# ================= TRACKING (IoU) =================
def compute_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1_p, y1_p, x2_p, y2_p = box2

    xi1 = max(x1, x1_p)
    yi1 = max(y1, y1_p)
    xi2 = min(x2, x2_p)
    yi2 = min(y2, y2_p)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_p - x1_p) * (y2_p - y2_p)

    union = box1_area + box2_area - inter_area

    return inter_area / union if union != 0 else 0


# ================= GUI =================
def show_results_page(status, count, conf=0):
    menu_frame.place_forget()
    results_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_label.config(
        text=f"FINAL STATUS: {status}",
        fg="#27ae60" if "DETECTED" in status else "#e74c3c"
    )
    count_label.config(text=f"Total Pipes Found: {count}")
    conf_label.config(text=f"Highest Confidence: {conf:.2f}")
    


def back_to_menu():
    results_frame.place_forget()
    menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)


# ================= DETECTION =================
def run_video_detection(is_live=False):
    def task():
        source = 0 if is_live else filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi")]
        )

        if source == "" and not is_live:
            return

        results = model.predict(
            source=source,
            show=True,
            stream=True,
            conf=0.3
        )

        tracked_boxes = []   # Store unique pipes
        max_conf = 0
        last_beep = 0

        for r in results:
            if len(r.boxes) > 0:
                boxes = r.boxes.xyxy.cpu().numpy()
                confs = r.boxes.conf.cpu().numpy()

                for box, conf in zip(boxes, confs):
                    x1, y1, x2, y2 = box
                    new_box = [x1, y1, x2, y2]

                    is_new = True

                    for tbox in tracked_boxes:
                        iou = compute_iou(new_box, tbox)
                        if iou > 0.5:   # SAME PIPE
                            is_new = False
                            break
                        

                    if is_new:
                        tracked_boxes.append(new_box)

                        #  Beep once per new pipe
                        if time.time() - last_beep > 1:
                            winsound.Beep(1000, 200)
                            last_beep = time.time()

                    if conf > max_conf:
                        max_conf = conf

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

        pipe_count = len(tracked_boxes)

        if pipe_count > 0:
            msg = f"🚨 ALERT!\nUnauthorized Pipe Detected\nCount: {pipe_count}\nConfidence: {max_conf:.2f}"
            send_telegram_alert(msg)
            generate_report("DETECTED", pipe_count, max_conf)

            show_results_page("UNAUTHORIZED PIPE DETECTED", pipe_count, max_conf)
            show_results_page("alert message send")

        else:
            generate_report("NORMAL", 0, 0)
            show_results_page("NORMAL PIPE (NO TARGET)", 0, 0)

    threading.Thread(target=task, daemon=True).start()


def check_image():
    path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.png *.jpeg")]
    )

    if path:
        results = model.predict(source=path, show=True, conf=0.3)

        r = results[0]
        count = len(r.boxes)

        if count > 0:
            max_conf = r.boxes.conf.max().item()

            winsound.Beep(1200, 300)

            msg = f"🚨 ALERT!\nPipe Detected in Image\nCount: {count}\nConfidence: {max_conf:.2f}"
            send_telegram_alert(msg)
            generate_report("DETECTED", count, max_conf)

            show_results_page("PIPE DETECTED", count, max_conf)
            
        else:
            generate_report("NORMAL", 0, 0)
            show_results_page("(NO TARGET)", 0, 0)


# ================= GUI SETUP =================
root = tk.Tk()
root.title("Sewer Detection System - YOLO")
root.state('zoomed')

bg_img = Image.open("background.png").resize(
    (root.winfo_screenwidth(), root.winfo_screenheight())
)
bg_photo = ImageTk.PhotoImage(bg_img)

tk.Label(root, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

menu_frame = tk.Frame(root, bg="#1a1a1a")
menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
tk.Label(menu_frame, image=bg_photo).place(relwidth=1, relheight=1)

tk.Label(
    menu_frame,
    text="DEEP LEARNING BASED SEWER DETECTION USING YOLO",
    font=("Helvetica", 28, "bold"),
    fg="white",
    bg="#1a1a1a"
).place(relx=0.5, rely=0.15, anchor="center")

btn_style = {"width": 30, "height": 2, "font": ("Arial", 14, "bold"), "fg": "white"}

tk.Button(menu_frame, text="LIVE CCTV DETECTION",
          command=lambda: run_video_detection(True),
          bg="#27ae60", **btn_style).place(relx=0.5, rely=0.35, anchor="center")

tk.Button(menu_frame, text="ANALYZE VIDEO FILE",
          command=lambda: run_video_detection(False),
          bg="#2980b9", **btn_style).place(relx=0.5, rely=0.50, anchor="center")

tk.Button(menu_frame, text="SCAN IMAGE",
          command=check_image,
          bg="#d35400", **btn_style).place(relx=0.5, rely=0.65, anchor="center")

# RESULTS PAGE
results_frame = tk.Frame(root, bg="#2c3e50", padx=50, pady=50)

tk.Label(results_frame, text="DETECTION SUMMARY",
         font=("Helvetica", 22, "bold"),
         fg="white", bg="#2c3e50").pack(pady=10)

count_label = tk.Label(results_frame, text="", font=("Helvetica", 18), fg="white", bg="#2c3e50")
count_label.pack()

status_label = tk.Label(results_frame, text="", font=("Helvetica", 18, "bold"), bg="#2c3e50")
status_label.pack(pady=10)

conf_label = tk.Label(results_frame, text="", font=("Helvetica", 14), fg="white", bg="#2c3e50")
conf_label.pack()

tk.Button(results_frame, text="BACK",
          command=back_to_menu,
          bg="#7f8c8d", fg="white", width=20).pack(pady=20)

root.mainloop()