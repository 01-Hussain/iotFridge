import os
import glob
from ultralytics import YOLO
train_folder_path = "runs/detect"

# Use glob to find the latest training session folder
latest_train_folder = max(glob.glob(os.path.join(train_folder_path, "train*")), key=os.path.getctime)


weights_path = os.path.join(latest_train_folder, "weights", "best.pt")

model = YOLO(weights_path)
results = model.train(data="config.yaml", epochs=40, imgsz=256)
