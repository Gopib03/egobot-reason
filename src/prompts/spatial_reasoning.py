cat > src/prompts/spatial_reasoning.py << 'EOF'
SYSTEM_PROMPT = (
    "You are the spatial awareness module of a mobile robot. "
    "You observe the world from a first-person camera. "
    "Your job is to understand the 3D layout and report positions."
)

SCENE_LAYOUT_PROMPT = """Analyze the spatial layout from the robot's egocentric camera.

Respond in JSON:
{
  "obstacles": [{"name": "", "position": "left|center|right", "distance": "near|mid|far"}],
  "free_paths": [],
  "key_objects": [{"name": "", "position": ""}],
  "people": [{"position": "", "activity": ""}]
}"""

TRAJECTORY_PREDICTION_PROMPT = """A moving object is visible from the robot's view.

Respond in JSON:
{
  "object": "",
  "direction": "toward|away|left_to_right|right_to_left|upward|downward",
  "approaching": false,
  "estimated_landing": "",
  "collision_risk": "none|low|medium|high"
}"""

DISTANCE_ESTIMATION_PROMPT = """Estimate the distance to the main subject.

Respond in JSON:
{
  "subject": "",
  "estimated_distance_meters": 0.0,
  "confidence": "low|medium|high",
  "reasoning": ""
}"""
EOF