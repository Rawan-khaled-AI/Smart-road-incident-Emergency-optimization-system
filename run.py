from src.pipeline import run_pipeline

file_path = "your_image_or_video.jpg"
result = run_pipeline(file_path, camera_id="CAM01")

print("Incident Detected:", result["incident_detected"])
print("Accident Frames:", result["accident_frames"])
print("Status:", result["status"])
print("Camera ID:", result["camera_id"])
print("Road Name:", result["road_name"])

print("Pothole Detected:", result["pothole_detected"])
print("Pothole Count:", result["pothole_count"])
print("Pothole Boxes:", result["pothole_boxes"])

if result["incident_detected"]:
    print("Nearest Ambulance:", result["ambulance_id"])
    print("Distance (km):", result["distance_km"])
    print("ETA (minutes):", result["eta_minutes"])
else:
    print("Nearest Ambulance: N/A")
    print("Distance (km): N/A")
    print("ETA (minutes): N/A")
