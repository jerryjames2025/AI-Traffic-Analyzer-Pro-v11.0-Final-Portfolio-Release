import os
import cv2
import time
import argparse
import subprocess

import config

from tracker import VehicleTracker
from counter import VehicleCounter
from analytics import draw_dashboard
from visualization import draw

from core.speed_estimator import SpeedEstimator
from core.vehicle_manager import VehicleManager
from core.exporter import Exporter
from core.violation_manager import ViolationManager
from core.session_manager import SessionManager


def convert_to_browser_video(input_video, output_video):
    print("Converting video to browser-compatible H264...", flush=True)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_video,
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        output_video
    ]

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        print("Browser video created:", flush=True)
        print(output_video, flush=True)

    except Exception as e:
        print("FFmpeg conversion failed.", flush=True)
        print(e, flush=True)


def process_video(video_path=None, show_window=True):
    # ---------------------------------
    # Select Video
    # ---------------------------------

    if video_path is None:
        video_path = config.VIDEO_PATH

    video_path = os.path.abspath(video_path)

    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Video file not found: {video_path}"
        )

    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    print("=" * 60, flush=True)
    print("AI Traffic Analyzer Started", flush=True)
    print("Video:", video_path, flush=True)
    print("=" * 60, flush=True)

    # ---------------------------------
    # Create Output Folders
    # ---------------------------------

    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(config.IMAGE_FOLDER, exist_ok=True)
    os.makedirs(config.ANALYTICS_FOLDER, exist_ok=True)
    os.makedirs(config.REPORT_FOLDER, exist_ok=True)

    # ---------------------------------
    # Initialize Components
    # ---------------------------------

    tracker = VehicleTracker(config)
    counter = VehicleCounter()

    session = SessionManager()
    current_session = session.create_session(video_name)

    print("=" * 60, flush=True)
    print("SESSION CREATED:", flush=True)
    print(current_session, flush=True)
    print("=" * 60, flush=True)

    manager = VehicleManager(session)
    violation_manager = ViolationManager(session)
    exporter = Exporter(session)

    speed_estimator = SpeedEstimator(
        fps=config.FPS,
        pixels_per_meter=config.PIXELS_PER_METER,
        history=config.SMOOTHING_HISTORY
    )

    vehicle_speeds = {}

    # ---------------------------------
    # Open Video
    # ---------------------------------

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError(
            f"Cannot open video: {video_path}"
        )

    fps_video = cap.get(cv2.CAP_PROP_FPS)

    if fps_video == 0:
        fps_video = config.FPS

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        total_frames = 1

    print(f"TOTAL_FRAMES:{total_frames}", flush=True)

    # ---------------------------------
    # Processed Video Output
    # ---------------------------------

    output_video = os.path.join(
        session.get_session(),
        "processed.mp4"
    )

    print("\nCreating processed video...", flush=True)
    print(output_video, flush=True)

    codec_list = [
        "mp4v",
        "avc1",
        "H264"
    ]

    writer = None

    for codec in codec_list:
        fourcc = cv2.VideoWriter_fourcc(*codec)

        writer = cv2.VideoWriter(
            output_video,
            fourcc,
            fps_video,
            (
                config.DISPLAY_WIDTH,
                config.DISPLAY_HEIGHT
            )
        )

        if writer.isOpened():
            print(f"Using codec : {codec}", flush=True)
            break

    if writer is None or not writer.isOpened():
        cap.release()

        raise RuntimeError(
            "Could not create processed video writer."
        )

    # ---------------------------------
    # Window
    # ---------------------------------

    if show_window:
        cv2.namedWindow(
            config.WINDOW_NAME,
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            config.WINDOW_NAME,
            config.WINDOW_WIDTH,
            config.WINDOW_HEIGHT
        )

    # ---------------------------------
    # Main Loop
    # ---------------------------------

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % 30 == 0 or frame_count == total_frames:
            print(
                f"PROGRESS:{frame_count}/{total_frames}",
                flush=True
            )

        frame = cv2.resize(
            frame,
            (
                config.DISPLAY_WIDTH,
                config.DISPLAY_HEIGHT
            )
        )

        start = time.time()

        result = tracker.track(frame)

        if result.boxes is not None:
            for box in result.boxes:
                if box.id is None:
                    continue

                cls = int(box.cls[0])

                if cls not in config.VEHICLE_CLASSES:
                    continue

                vehicle_class = config.VEHICLE_CLASSES[cls]
                vehicle_id = int(box.id[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                center = (
                    (x1 + x2) // 2,
                    y2
                )

                # ---------------------------------
                # Speed
                # ---------------------------------

                speed = speed_estimator.update(
                    vehicle_id,
                    center
                )

                vehicle_speeds[vehicle_id] = speed

                # ---------------------------------
                # Counter
                # ---------------------------------

                counter.update(
                    vehicle_id,
                    vehicle_class
                )

                # ---------------------------------
                # Vehicle Manager
                # ---------------------------------

                vehicle = manager.update_vehicle(
                    vehicle_id,
                    vehicle_class,
                    center,
                    speed,
                    frame,
                    (x1, y1, x2, y2),
                    float(box.conf[0])
                )

                # ---------------------------------
                # Violations
                # ---------------------------------

                if vehicle.overspeed:
                    violation_manager.add_overspeed(
                        vehicle,
                        frame,
                        (x1, y1, x2, y2)
                    )

        # ---------------------------------
        # Draw
        # ---------------------------------

        frame = draw(
            frame,
            result,
            config,
            vehicle_speeds,
            manager
        )

        frame = draw_dashboard(
            frame,
            counter.get_counts()
        )

        # ---------------------------------
        # FPS
        # ---------------------------------

        elapsed = time.time() - start
        fps = 0 if elapsed <= 0 else 1 / elapsed

        cv2.putText(
            frame,
            f"FPS : {fps:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # ---------------------------------
        # Save Output
        # ---------------------------------

        writer.write(frame)

        if show_window:
            cv2.imshow(
                config.WINDOW_NAME,
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # ---------------------------------
    # Cleanup
    # ---------------------------------

    cap.release()
    writer.release()

    if show_window:
        cv2.destroyAllWindows()

    # ---------------------------------
    # Browser Video
    # ---------------------------------

    browser_video = os.path.join(
        session.get_session(),
        "processed_browser.mp4"
    )

    convert_to_browser_video(
        output_video,
        browser_video
    )

    # ---------------------------------
    # Export Files
    # ---------------------------------

    if config.SAVE_JSON:
        exporter.export_json(
            manager.get_all()
        )

    if config.SAVE_CSV:
        exporter.export_csv(
            manager.get_all()
        )

    exporter.export_summary(manager)
    violation_manager.export()

    print("\nProcessing Finished Successfully.", flush=True)
    print("Session:", flush=True)
    print(session.get_session(), flush=True)
    print(f"SESSION_PATH:{session.get_session()}", flush=True)

    return session.get_session()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AI Traffic Analyzer Pro"
    )

    parser.add_argument(
        "--video",
        type=str,
        default=None,
        help="Path to input traffic video"
    )

    parser.add_argument(
        "--no-window",
        action="store_true",
        help="Run without OpenCV display window"
    )

    args = parser.parse_args()

    process_video(
        video_path=args.video,
        show_window=not args.no_window
    )