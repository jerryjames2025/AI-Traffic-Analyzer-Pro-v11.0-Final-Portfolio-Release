from ultralytics import YOLO


class VehicleTracker:

    def __init__(self, config):

        print("Loading YOLO Model...")

        self.model = YOLO(config.MODEL_NAME)

        print("Model Loaded Successfully")

        self.config = config

    def track(self, frame):

        results = self.model.track(

            frame,

            persist=True,

            tracker=self.config.TRACKER,

            device=self.config.DEVICE,

            conf=self.config.CONFIDENCE,

            iou=self.config.IOU,

            verbose=False

        )

        return results[0]