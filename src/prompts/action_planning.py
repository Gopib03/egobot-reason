cat > src/prompts/action_planning.py << 'EOF'
SYSTEM_PROMPT = (
    "You are the decision-making module of an assistive robot. "
    "Based on egocentric observations, decide the next action. "
    "Be safe, helpful, and precise."
)

NEXT_ACTION_PROMPT = """Based on this egocentric robot view, determine the best next action.

Respond in JSON:
{
  "scene_summary": "",
  "human_interaction_needed": false,
  "safety_ok": true,
  "next_action": "",
  "action_description": "",
  "priority": "low|medium|high|urgent"
}"""

GRIPPER_TRAJECTORY_PROMPT = """You are given the task: "{task}"

From this egocentric view, specify the 2D trajectory for the robot gripper in pixel space.
Coordinates normalized to 0-1000. Origin is top-left. X=right, Y=down.

Respond in JSON:
{{
  "trajectory": [{{"point_2d": [0, 0], "label": ""}}],
  "task": "",
  "feasibility": "feasible|difficult|infeasible",
  "notes": ""
}}"""

MULTI_STEP_PLAN_PROMPT = """Create a multi-step plan to accomplish: "{task}"

Respond in JSON:
{{
  "task": "",
  "steps": [
    {{"step_number": 1, "action": "", "completion_check": "", "safety_note": null}}
  ],
  "estimated_total_steps": 0
}}"""
EOF