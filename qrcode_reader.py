from ultralytics import YOLO
model = YOLO(r"C:\Users\HP\PycharmProjects\pythonProject1\yolo\runs\detect\train2\weights\best.pt")
results = model(r'C:\Users\HP\PycharmProjects\pythonProject1\smart_fridge\test.jpg',save=True,conf=0.7,imgsz=256)[0]