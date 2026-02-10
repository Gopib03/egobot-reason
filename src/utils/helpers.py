cat > src/utils/helpers.py << 'EOF'
import os
import base64
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass
class Config:
    nvidia_api_key: str = field(default_factory=lambda: os.getenv("NVIDIA_API_KEY", ""))
    cosmos_model: str = field(default_factory=lambda: os.getenv("COSMOS_MODEL", "nvidia/cosmos-reason2-8b"))
    cosmos_base_url: str = field(default_factory=lambda: os.getenv("COSMOS_BASE_URL", "https://integrate.api.nvidia.com/v1"))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "4096")))
    temperature: float = field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.3")))
    top_p: float = field(default_factory=lambda: float(os.getenv("TOP_P", "0.3")))
    video_fps: int = field(default_factory=lambda: int(os.getenv("VIDEO_FPS", "2")))

    def validate(self):
        if not self.nvidia_api_key:
            raise ValueError(
                "NVIDIA_API_KEY is required. "
                "Get one at https://build.nvidia.com/settings/api-keys"
            )


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_media_type(file_path):
    ext = Path(file_path).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".mp4": "video/mp4",
    }
    return mime_map.get(ext, "application/octet-stream")
EOF