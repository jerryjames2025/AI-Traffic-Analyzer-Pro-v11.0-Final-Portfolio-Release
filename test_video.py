import cv2

cap = cv2.VideoCapture(
    "sessions/20260705_155347_traffic/processed.mp4"
)

print("Opened:", cap.isOpened())

print("FPS:", cap.get(cv2.CAP_PROP_FPS))

print("Width:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))

print("Height:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("Frames:", cap.get(cv2.CAP_PROP_FRAME_COUNT))

cap.release()