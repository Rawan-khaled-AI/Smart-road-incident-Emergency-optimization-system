import os
import sys

import cv2
import streamlit as st

from src.pipeline import run_pipeline

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

st.set_page_config(page_title="Smart Road Incident Dashboard", layout="wide")


def draw_all_boxes(image_path, accident_boxes, pothole_boxes):
    image = cv2.imread(image_path)
    if image is None:
        return None

    for det in accident_boxes:
        x1, y1, x2, y2 = map(int, det["box"])
        label = f'ACCIDENT ({det["confidence"]:.2f})'

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(
            image,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )

    for det in pothole_boxes:
        x1, y1, x2, y2 = map(int, det["box"])
        label = f'POTHOLE ({det["confidence"]:.2f})'

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(
            image,
            label,
            (x1, max(y1 - 10, 40)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
        )

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


st.title("Smart Road Incident Emergency Optimization System")
st.write(
    "Upload a road image or video, then analyze it for accident detection, "
    "pothole detection, and ambulance dispatch."
)

uploaded_file = st.file_uploader(
    "Upload Image or Video",
    type=["jpg", "jpeg", "png", "mp4", "avi", "mov"],
)

camera_id = st.selectbox("Select Camera ID", ["CAM01", "CAM02", "CAM03"])

if uploaded_file is not None:
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"File uploaded successfully: {uploaded_file.name}")

    is_image = uploaded_file.type.startswith("image")
    is_video = uploaded_file.type.startswith("video")

    if is_image:
        st.image(file_path, caption="Uploaded Image", use_container_width=True)
    elif is_video:
        st.video(file_path)

    if st.button("Run Analysis"):
        with st.spinner("Analyzing..."):
            result = run_pipeline(file_path, camera_id)

        st.subheader("Analysis Result")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Incident Detected",
                "Yes" if result["incident_detected"] else "No",
            )

        with col2:
            pothole_status = (
                "Unavailable"
                if result.get("pothole_error")
                else ("Yes" if result["pothole_detected"] else "No")
            )
            st.metric("Pothole Detected", pothole_status)

        with col3:
            st.metric("Status", result["status"])

        with col4:
            st.metric("Camera ID", result["camera_id"])

        st.write(f"**Road Name:** {result['road_name']}")

        if is_video:
            frames = result["accident_frames"]
            st.write(f"**Accident Frames Count:** {len(frames)}")

            if len(frames) <= 20:
                st.write(f"**Accident Frames:** {frames}")
            else:
                st.write(f"**Accident Frames (first 20):** {frames[:20]} ...")
        else:
            detection_text = (
                "Accident detected in uploaded image"
                if result["incident_detected"]
                else "No accident detected"
            )
            st.write(f"**Detection Result:** {detection_text}")

        st.subheader("Road Condition Information")

        if result.get("pothole_error"):
            st.warning("Pothole model is currently unavailable.")
            with st.expander("Show pothole model error"):
                st.code(result["pothole_error"])
        else:
            st.write(f"**Pothole Count:** {result['pothole_count']}")

            if is_image and (
                result["incident_detected"] or result["pothole_detected"]
            ):
                annotated = draw_all_boxes(
                    file_path,
                    result["accident_boxes"],
                    result["pothole_boxes"],
                )
                if annotated is not None:
                    st.image(
                        annotated,
                        caption="Annotated Detection Result",
                        use_container_width=True,
                    )

            if result["pothole_detected"]:
                st.success("Potholes detected on the road.")
            else:
                st.info("No potholes detected.")

        if result["incident_detected"]:
            st.subheader("Dispatch Information")
            st.write(f"**Nearest Ambulance:** {result['ambulance_id']}")
            st.write(f"**Distance:** {result['distance_km']} km")
            st.write(f"**ETA:** {result['eta_minutes']} minutes")
        else:
            st.info("No ambulance dispatch needed.")

        with st.expander("Show detailed detections"):
            st.write("**Accident Boxes:**")
            st.json(result["accident_boxes"])

            if result.get("pothole_error"):
                st.write("**Pothole Model Error:**")
                st.code(result["pothole_error"])
            else:
                st.write("**Pothole Boxes:**")
                st.json(result["pothole_boxes"])
