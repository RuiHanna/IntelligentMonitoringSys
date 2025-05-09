import cv2
import time
from tqdm import tqdm


def process_video(filepath, tracker):
    """处理视频文件并返回跟踪结果"""
    cap = cv2.VideoCapture(filepath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    tracks = []
    start_time = time.time()

    for _ in tqdm(range(total_frames), desc="Processing video"):
        ret, frame = cap.read()
        if not ret:
            break

        # 执行目标跟踪
        frame_results = tracker.update(frame)
        tracks.extend(frame_results)

    cap.release()

    return {
        'processing_time': time.time() - start_time,
        'total_frames': total_frames,
        'fps': fps,
        'tracks': tracks
    }