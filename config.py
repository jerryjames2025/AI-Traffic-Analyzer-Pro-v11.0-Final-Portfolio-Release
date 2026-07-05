import torch

# -------------------------------------------------
# Video
# -------------------------------------------------

VIDEO_PATH = "videos/traffic.mp4"

WINDOW_NAME = "AI Traffic Analyzer Pro"

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

# -------------------------------------------------
# Model
# -------------------------------------------------

MODEL_NAME = "yolov8s.pt"

DEVICE = 0 if torch.cuda.is_available() else "cpu"

CONFIDENCE = 0.35

IOU = 0.45

# -------------------------------------------------
# Tracking
# -------------------------------------------------

TRACKER = "bytetrack.yaml"

# -------------------------------------------------
# Vehicle Classes (COCO)
# -------------------------------------------------

VEHICLE_CLASSES = {

    2: "Car",

    3: "Motorcycle",

    5: "Bus",

    7: "Truck"

}

# -------------------------------------------------
# Colors
# -------------------------------------------------

COLORS = {

    "Car": (0,255,0),

    "Motorcycle": (255,200,0),

    "Bus": (255,0,255),

    "Truck": (0,150,255)

}

# -------------------------------------------------
# Speed

# These values can be calibrated later
# -------------------------------------------------

FPS = 30

PIXELS_PER_METER = 12

SMOOTHING_HISTORY = 8

SPEED_LIMIT = 60

# -------------------------------------------------
# Saving
# -------------------------------------------------

SAVE_VIDEO = True

SAVE_IMAGES = True

SAVE_JSON = True

SAVE_CSV = True

# -------------------------------------------------
# Directories
# -------------------------------------------------

OUTPUT_FOLDER = "outputs"

IMAGE_FOLDER = "vehicle_images"

ANALYTICS_FOLDER = "analytics"

REPORT_FOLDER = "reports"