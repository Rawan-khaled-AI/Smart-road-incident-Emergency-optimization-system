from ultralytics import YOLO

model = None
model_error = None

try:
    model = YOLO("models/pothole.pt")
except Exception as e:
    model_error = str(e)


def detect_pothole(file_path):
    if model is None:
        return {
            "pothole_detected": False,
            "pothole_count": 0,
            "pothole_boxes": [],
            "pothole_error": model_error,
        }

    results = model(file_path)

    detections = []
    pothole_count = 0

    for frame_idx, r in enumerate(results):
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()

            detections.append(
                {
                    "class": (
                        model.names[cls]
                        if hasattr(model, "names")
                        else "pothole"
                    ),
                    "confidence": round(conf, 3),
                    "box": [round(x, 2) for x in xyxy],
                    "frame": frame_idx,
                }
            )
            pothole_count += 1

    return {
        "pothole_detected": pothole_count > 0,
        "pothole_count": pothole_count,
        "pothole_boxes": detections,
        "pothole_error": None,
    }
