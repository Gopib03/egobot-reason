cat > src/core/action_planner.py << 'EOF'
from src.core.cosmos_client import CosmosClient
from src.core.reasoning_engine import ReasoningEngine
from src.prompts import action_planning
from src.utils.helpers import Config


class ActionPlanner:
    def __init__(self, config=None):
        self.config = config or Config()
        self.client = CosmosClient(self.config)
        self.engine = ReasoningEngine(self.config)

    def plan_gripper_trajectory(self, image_path, task):
        prompt = action_planning.GRIPPER_TRAJECTORY_PROMPT.format(task=task)
        result = self.client.reason_about_image(
            image_path=image_path, prompt=prompt,
            system_prompt=action_planning.SYSTEM_PROMPT, enable_reasoning=True,
        )
        return self.engine._format_result("gripper_trajectory", result)

    def plan_multi_step(self, image_path, task):
        prompt = action_planning.MULTI_STEP_PLAN_PROMPT.format(task=task)
        result = self.client.reason_about_image(
            image_path=image_path, prompt=prompt,
            system_prompt=action_planning.SYSTEM_PROMPT, enable_reasoning=True,
        )
        return self.engine._format_result("multi_step_plan", result)
EOF