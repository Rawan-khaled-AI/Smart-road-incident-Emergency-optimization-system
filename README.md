# 🚑 Smart Road Incident Emergency Optimization System

An AI-powered system that detects road accidents and potholes from images or videos, then automatically dispatches the nearest ambulance.

---

## 📌 Overview

This project combines **Computer Vision + Decision Systems** to improve emergency response time on roads.

The system analyzes uploaded media and:
- Detects accidents
- Detects potholes (if model available)
- Finds nearest ambulance
- Calculates distance & ETA
- Displays results in an interactive dashboard

---

## 🎯 Features

- 🚗 Accident detection using YOLO
- 🕳️ Pothole detection (optional)
- 🚑 Automatic ambulance dispatch
- 📍 Location-based decision system
- ⏱️ Distance & ETA calculation
- 🖥️ Interactive Streamlit dashboard

---

## 🧠 How It Works

1. Upload image or video
2. Detect accident using YOLO model
3. Detect potholes (if model available)
4. Get camera location
5. Find nearest ambulance
6. Calculate distance and ETA
7. Display results on dashboard

---

## 🖼️ Demo

### Dashboard
![Dashboard](assests/Screenshot%202026-03-25%20095008.png)

### Detection Output
![Detection](assests/Screenshot%202026-03-25%20095112.png)

### Results
![Results](assests/Screenshot%202026-03-25%20095144.png)

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Ultralytics YOLO
- OpenCV
- Pandas

---

## 🚀 Installation & Run

### 1. Clone the repository
```bash
git clone https://github.com/Rawan-khaled-AI/Smart-road-incident-Emergency-optimization-system.git
cd Smart-road-incident-Emergency-optimization-system