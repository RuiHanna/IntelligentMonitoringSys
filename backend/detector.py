# detector.py

import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import time
import os

model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=30)


def process_video(path, detection_thresh=0.5, max_targets=20):
    cap = cv2.VideoCapture(path)
    tracked_results = []

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    fps = cap.get(cv2.CAP_PROP_FPS)
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_path = os.path.join('output', os.path.basename(path).replace(".", "_tracked."))

    os.makedirs('output', exist_ok=True)
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)[0]
        detections = []
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, cls_id = r
            if score > detection_thresh:
                detections.append(([x1, y1, x2 - x1, y2 - y1], score, int(cls_id)))

        detections = sorted(detections, key=lambda x: x[1], reverse=True)[:max_targets]
        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            l, t, r, b = track.to_ltrb()
            tracked_results.append({
                "track_id": track_id,
                "bbox": [l, t, r, b],
                "timestamp": time.time()
            })
            cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {track_id}', (int(l), int(t) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()

    if not is_browser_friendly(output_path):
        convert_to_h264(output_path)

    return tracked_results


def generate_tracking_stream(detection_thresh=0.5, max_targets=20):
    tracker = DeepSort(max_age=30, max_iou_distance=0.7, n_init=3)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detections = []
        yolo_results = model(frame)[0]
        for r in yolo_results.boxes.data.tolist():
            x1, y1, x2, y2, score, cls_id = r
            if score >= detection_thresh:
                detections.append(([x1, y1, x2 - x1, y2 - y1], score, int(cls_id)))

        tracks = tracker.update_tracks(detections, frame=frame)
        timestamp = time.time()

        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            l, t, r, b = track.to_ltrb()
            cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (0, 255, 0), 2)
            cv2.putText(frame, f'ID:{track_id}', (int(l), int(t) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # 编码为 JPEG 并 yield
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()


def is_browser_friendly(video_path):
    cap = cv2.VideoCapture(video_path)
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))
    cap.release()
    return codec == cv2.VideoWriter_fourcc(*'avc1')


def convert_to_h264(input_path):
    output_path = input_path.replace(".mp4", "_converted.mp4")
    os.system(f'ffmpeg -i "{input_path}" -c:v libx264 -c:a aac -movflags +faststart "{output_path}"')
    os.replace(output_path, input_path)
