cat > src/core/reasoning_engine.py << 'EOF'
import json
import logging
from src.core.cosmos_client import CosmosClient
from src.core.video_processor import VideoProcessor
from src.prompts import social_reasoning, spatial_reasoning, safety_assessment, action_planning
from src.utils.helpers import Config

logger = logging.getLogger(__name__)

REASONING_MODES = {
    "social": (social_reasoning.SYSTEM_PROMPT, social_reasoning.SOCIAL_INTENT_PROMPT),
    "handover": (social_reasoning.SYSTEM_PROMPT, social_reasoning.HANDOVER_DETECTION_PROMPT),
    "spatial": (spatial_reasoning.SYSTEM_PROMPT, spatial_reasoning.SCENE_LAYOUT_PROMPT),
    "trajectory": (spatial_reasoning.SYSTEM_PROMPT, spatial_reasoning.TRAJECTORY_PREDICTION_PROMPT),
    "safety": (safety_assessment.SYSTEM_PROMPT, safety_assessment.SAFETY_ASSESSMENT_PROMPT),
    "thrown_object": (safety_assessment.SYSTEM_PROMPT, safety_assessment.THROWN_OBJECT_SAFETY_PROMPT),
    "planning": (action_planning.SYSTEM_PROMPT, action_planning.NEXT_ACTION_PROMPT),
}


class ReasoningEngine:
    def __init__(self, config=None):
        self.config = config or Config()
        self.client = CosmosClient(self.config)
        self.video_processor = VideoProcessor(self.config)

    def analyze_image(self, image_path, mode="social"):
        system_prompt, user_prompt = self._get_prompts(mode)
        result = self.client.reason_about_image(
            image_path=image_path, prompt=user_prompt,
            system_prompt=system_prompt, enable_reasoning=True,
        )
        return self._format_result(mode, result)

    def analyze_image_url(self, image_url, mode="social"):
        system_prompt, user_prompt = self._get_prompts(mode)
        result = self.client.reason_about_image_url(
            image_url=image_url, prompt=user_prompt,
            system_prompt=system_prompt, enable_reasoning=True,
        )
        return self._format_result(mode, result)

    def analyze_video(self, video_path, mode="social", max_frames=16):
        video_info = self.video_processor.get_video_info(video_path)
        frames = self.video_processor.extract_frames(video_path, max_frames=max_frames)
        if not frames:
            raise ValueError(f"No frames extracted from {video_path}")
        system_prompt, user_prompt = self._get_prompts(mode)
        result = self.client.reason_about_frames(
            frame_paths=frames, prompt=user_prompt,
            system_prompt=system_prompt, enable_reasoning=True,
        )
        output = self._format_result(mode, result)
        output["video_info"] = video_info
        output["frames_analyzed"] = len(frames)
        return output

    def full_analysis(self, image_path):
        results = {}
        for mode in ["social", "spatial", "safety", "planning"]:
            try:
                results[mode] = self.analyze_image(image_path, mode=mode)
            except Exception as e:
                results[mode] = {"error": str(e)}
        return {"type": "full_analysis", "image": image_path, "results": results}

    @staticmethod
    def _get_prompts(mode):
        if mode not in REASONING_MODES:
            raise ValueError(f"Unknown mode '{mode}'. Available: {', '.join(REASONING_MODES.keys())}")
        return REASONING_MODES[mode]

    @staticmethod
    def _format_result(mode, result):
        parsed = None
        answer = result.get("answer", "")
        try:
            clean = answer.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1] if "\n" in clean else clean[3:]
                clean = clean.rsplit("```", 1)[0]
            parsed = json.loads(clean)
        except (json.JSONDecodeError, IndexError):
            pass
        return {
            "mode": mode,
            "reasoning": result.get("reasoning", ""),
            "answer": answer,
            "parsed": parsed,
            "usage": result.get("usage", {}),
        }

    @staticmethod
    def available_modes():
        return list(REASONING_MODES.keys())
EOF