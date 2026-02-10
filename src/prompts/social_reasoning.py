cat > src/prompts/social_reasoning.py << 'EOF'
SYSTEM_PROMPT = (
    "You are the vision system of an assistive robot. "
    "You observe the world from a first-person (egocentric) camera. "
    "Your job is to interpret human social behavior directed at you "
    "and provide structured reasoning about the person's intent."
)

SOCIAL_INTENT_PROMPT = """Analyze this egocentric image from a robot's camera.

Determine:
1. People present: How many? Where relative to the robot?
2. Social engagement: Is anyone engaging with the robot?
3. Gesture classification: (waving, pointing, reaching, handing object, stop signal, beckoning, none)
4. Intent: (handover, attention, help, avoidance, no interaction)
5. Confidence: (low / medium / high)

Respond in JSON:
{
  "people_count": 0,
  "engaged_with_robot": false,
  "gestures": [],
  "intent": "",
  "intent_description": "",
  "confidence": ""
}"""

HANDOVER_DETECTION_PROMPT = """From this robot's egocentric view, determine if a human is trying to hand an object to the robot.

Respond in JSON:
{
  "handover_detected": false,
  "object": null,
  "distance": "near|medium|far",
  "clarity": "clear|ambiguous|none"
}"""

ENGAGEMENT_LEVEL_PROMPT = """From this egocentric robot view, rate the level of human engagement.

Respond in JSON:
{
  "engagement_level": "none|passive|active|urgent",
  "cues": [],
  "recommended_robot_response": "ignore|acknowledge|approach|assist|stop"
}"""
EOF