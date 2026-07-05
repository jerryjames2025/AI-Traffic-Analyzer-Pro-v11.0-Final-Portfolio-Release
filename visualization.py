import cv2


def draw(frame, result, config, speeds, manager):

    if result.boxes is None:
        return frame

    for box in result.boxes:

        if box.id is None:
            continue

        cls = int(box.cls[0])

        if cls not in config.VEHICLE_CLASSES:
            continue

        vehicle_class = config.VEHICLE_CLASSES[cls]
        vehicle_id = int(box.id[0])
        confidence = float(box.conf[0])

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )

        color = config.COLORS.get(
            vehicle_class,
            (0, 255, 0)
        )

        speed = speeds.get(
            vehicle_id,
            0
        )

        vehicle = manager.get_vehicle(
            vehicle_id
        )

        overspeed = False
        number_plate = "Not Detected"

        if vehicle is not None:

            overspeed = vehicle.overspeed
            number_plate = vehicle.number_plate

        if overspeed:
            color = (0, 0, 255)

        # -----------------------------
        # Bounding Box
        # -----------------------------

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # -----------------------------
        # Header
        # -----------------------------

        header_height = 88

        top_y = max(
            0,
            y1 - header_height
        )

        cv2.rectangle(
            frame,
            (x1, top_y),
            (x2, y1),
            color,
            -1
        )

        cv2.putText(
            frame,
            f"{vehicle_class} | ID: {vehicle_id}",
            (x1 + 5, top_y + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Speed: {speed:.1f} km/h",
            (x1 + 5, top_y + 43),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Plate: {number_plate}",
            (x1 + 5, top_y + 66),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.50,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"{confidence * 100:.0f}%",
            (x2 - 55, y2 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2
        )

        # -----------------------------
        # Center
        # -----------------------------

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        cv2.circle(
            frame,
            (cx, cy),
            4,
            (0, 255, 255),
            -1
        )

        # -----------------------------
        # Trail
        # -----------------------------

        if vehicle is not None:

            points = vehicle.positions

            if len(points) >= 2:

                for i in range(
                    1,
                    len(points)
                ):

                    cv2.line(
                        frame,
                        points[i - 1],
                        points[i],
                        color,
                        2
                    )

        # -----------------------------
        # Overspeed Warning
        # -----------------------------

        if overspeed:

            cv2.putText(
                frame,
                "OVERSPEED",
                (x1, y2 + 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.70,
                (0, 0, 255),
                2
            )

    return frame