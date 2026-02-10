
SYSTEM_PROMPT = (
    "You are the safety monitoring system of a mobile robot. "
    "Your top priority is preventing harm to humans and property. "
    "You observe from a first-person camera and assess risks."
)

SAFETY_ASSESSMENT_PROMPT = """Perform a safety assessment from the robot's egocentric camera.

Respond in JSON:
{
  "hazards": [{"type": "", "severity": "low|medium|high|critical", "location": ""}],
  "collision_risk": "none|low|medium|high|imminent",
  "human_safety_concern": false,
  "environmental_hazards": [],
  "recommended_action": "continue|slow_down|stop|reverse|reroute",
  "explanation": ""
}"""

THROWN_OBJECT_SAFETY_PROMPT = """An object appears to be in motion from the robot's view.

Respond in JSON:
{
  "object": "",
  "moving_toward_robot": false,
  "hit_risk": "none|low|medium|high",
  "evasive_action_needed": false,
  "recommended_action": "stay|duck|move_left|move_right|back_up"
}"""
