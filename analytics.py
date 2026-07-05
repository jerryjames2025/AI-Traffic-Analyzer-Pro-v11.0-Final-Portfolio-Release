import cv2


def draw_dashboard(frame, counts):

    # ---------------------------------------
    # Background Panel
    # ---------------------------------------

    cv2.rectangle(
        frame,
        (10, 70),
        (360, 280),
        (35, 35, 35),
        -1
    )

    cv2.rectangle(
        frame,
        (10, 70),
        (360, 280),
        (255, 255, 255),
        2
    )

    # ---------------------------------------
    # Title
    # ---------------------------------------

    cv2.putText(
        frame,
        "Traffic Analytics",
        (25, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # ---------------------------------------
    # Vehicle Counts
    # ---------------------------------------

    total = sum(counts.values())

    car = counts.get("Car", 0)
    bike = counts.get("Motorcycle", 0)
    bus = counts.get("Bus", 0)
    truck = counts.get("Truck", 0)

    cv2.putText(
        frame,
        f"Total Vehicles : {total}",
        (25, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,255),
        2
    )

    cv2.putText(
        frame,
        f"Cars          : {car}",
        (25,165),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0,255,0),
        2
    )

    cv2.putText(
        frame,
        f"Motorcycles   : {bike}",
        (25,195),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,0),
        2
    )

    cv2.putText(
        frame,
        f"Buses         : {bus}",
        (25,225),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,0,255),
        2
    )

    cv2.putText(
        frame,
        f"Trucks        : {truck}",
        (25,255),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0,165,255),
        2
    )

    return frame