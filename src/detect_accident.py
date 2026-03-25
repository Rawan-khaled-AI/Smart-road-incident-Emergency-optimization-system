from ultralytics import YOLO

model = YOLO("models/accident.pt")


def detect_accident(file_path):
    results = model(file_path, conf=0.5)

    accident_boxes = []
    accident_frames = []
    incident_detected = False

    for frame_idx, r in enumerate(results):
        if r.boxes is None:
            continue

        frame_has_accident = False

        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()

            accident_boxes.append(
                {
                    "class": (
                        model.names[cls]
                        if hasattr(model, "names")
                        else "accident"
                    ),
                    "confidence": round(conf, 3),
                    "box": [round(x, 2) for x in xyxy],
                    "frame": frame_idx,
                }
            )
            frame_has_accident = True
            incident_detected = True

        if frame_has_accident:
            accident_frames.append(frame_idx)

    return {
        "incident_detected": incident_detected,
        "accident_frames": accident_frames,
        "accident_boxes": accident_boxes,
    }
