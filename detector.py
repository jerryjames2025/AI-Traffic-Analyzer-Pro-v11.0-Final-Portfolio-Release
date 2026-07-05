from ultralytics import YOLO
import cv2


class VehicleDetector:

    def __init__(self, config):

        self.config = config

        print("Loading YOLO model...")

        self.model = YOLO(config.MODEL_PATH)

        print("Model Loaded Successfully!")

    def detect(self, frame):

        results = self.model.predict(

            source=frame,

            device=self.config.DEVICE,

            imgsz=self.config.IMAGE_SIZE,

            conf=self.config.CONFIDENCE,

            verbose=False

        )

        detections = []

        result = results[0]

        for box in result.boxes:

            cls = int(box.cls[0])

            if cls not in self.config.VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({

                "class": self.config.VEHICLE_CLASSES[cls],

                "confidence": float(box.conf[0]),

                "bbox": (x1, y1, x2, y2)

            })

        return detections