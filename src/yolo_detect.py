# src/yolo_detect.py
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--output", default="outputs/detections.json")
    args = parser.parse_args()
    # placeholder: هنا ستضعون كود inference لYOLO
    print(f"Run YOLO on {args.video} and save to {args.output}")

if __name__ == "__main__":
    main()
