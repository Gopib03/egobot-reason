
import logging
import tempfile
from pathlib import Path
import cv2
from src.utils.helpers import Config

logger = logging.getLogger(__name__)


class VideoProcessor:
    def __init__(self, config=None):
        self.config = config or Config()

    def extract_frames(self, video_path, output_dir=None, max_frames=16):
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        native_fps = cap.get(cv2.CAP_PROP_FPS)
        target_fps = min(self.config.video_fps, native_fps)
        frame_interval = max(1, int(native_fps / target_fps))

        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="egobot_frames_")
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        extracted = []
        frame_idx = 0
        while cap.isOpened() and len(extracted) < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_interval == 0:
                out_path = str(Path(output_dir) / f"frame_{frame_idx:06d}.jpg")
                cv2.imwrite(out_path, frame)
                extracted.append(out_path)
            frame_idx += 1

        cap.release()
        logger.info("Extracted %d frames from %s", len(extracted), video_path)
        return extracted

    @staticmethod
    def get_video_info(video_path):
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")
        info = {
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }
        info["duration_sec"] = info["frame_count"] / info["fps"] if info["fps"] > 0 else 0
        cap.release()
        return info
