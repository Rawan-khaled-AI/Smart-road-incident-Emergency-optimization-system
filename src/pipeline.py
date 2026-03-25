import pandas as pd

from src.detect_accident import detect_accident
from src.detect_pothole import detect_pothole
from src.dispatch import find_nearest_ambulance


def get_camera_location(camera_id):
    cameras = pd.read_csv("data/camera_locations.csv")
    row = cameras[cameras["camera_id"] == camera_id].iloc[0]
    return row["lat"], row["lon"], row["road"]


def run_pipeline(file_path, camera_id="CAM01"):
    camera_lat, camera_lon, road_name = get_camera_location(camera_id)

    accident_result = detect_accident(file_path)
    pothole_result = detect_pothole(file_path)

    incident = accident_result["incident_detected"]
    frames = accident_result["accident_frames"]

    result = {
        "incident_detected": incident,
        "accident_frames": frames,
        "accident_boxes": accident_result["accident_boxes"],
        "ambulance_id": None,
        "distance_km": None,
        "eta_minutes": None,
        "status": "No Incident",
        "camera_id": camera_id,
        "road_name": road_name,
        "pothole_error": pothole_result.get("pothole_error"),
        "pothole_detected": pothole_result["pothole_detected"],
        "pothole_count": pothole_result["pothole_count"],
        "pothole_boxes": pothole_result["pothole_boxes"],
    }

    if incident:
        amb, dist, eta = find_nearest_ambulance(camera_lat, camera_lon)
        result["ambulance_id"] = amb
        result["distance_km"] = round(dist, 2)
        result["eta_minutes"] = round(eta, 2)
        result["status"] = "Ambulance Dispatched"

    return result
