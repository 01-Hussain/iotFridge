from ultralytics import YOLO
import glob
import os
train_folder_path = "runs/detect"

latest_train_folder = max(glob.glob(os.path.join(train_folder_path, "train*")), key=os.path.getctime)


weights_path = os.path.join(latest_train_folder, "weights", "best.pt")

model = YOLO(weights_path)

results = model('try.jpg',conf=0.5,imgsz=256)[0]
for detection in results.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = detection
    print(int(class_id))
