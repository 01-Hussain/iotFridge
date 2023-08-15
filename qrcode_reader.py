from ultralytics import YOLO
import glob
import os
model_directory = r"C:\Users\HP\Downloads\iotFridge-main\iotFridge-main\runs\detect"

model_files = glob.glob(f"{model_directory}/train*/weights/best.pt")
latest_model_file = max(model_files, key=os.path.getctime)
model = YOLO(latest_model_file)

results = model('try.jpg',conf=0.5,imgsz=256)[0]
for detection in results.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = detection
    print(int(class_id))
