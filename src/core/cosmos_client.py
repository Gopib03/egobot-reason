cat > src/core/cosmos_client.py << 'EOF'
import logging
from openai import OpenAI
from src.utils.helpers import Config, encode_image_to_base64, get_media_type

logger = logging.getLogger(__name__)


class CosmosClient:
    def __init__(self, config=None):
        self.config = config or Config()
        self.config.validate()
        self.client = OpenAI(
            base_url=self.config.cosmos_base_url,
            api_key=self.config.nvidia_api_key,
        )

    def reason_about_image(self, image_path, prompt, system_prompt="You are a helpful robot reasoning assistant.", enable_reasoning=True):
        b64 = encode_image_to_base64(image_path)
        media_type = get_media_type(image_path)
        data_uri = f"data:{media_type};base64,{b64}"
        full_prompt = self._maybe_add_reasoning_tag(prompt, enable_reasoning)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": data_uri}},
                {"type": "text", "text": full_prompt},
            ]},
        ]
        return self._call(messages)

    def reason_about_image_url(self, image_url, prompt, system_prompt="You are a helpful robot reasoning assistant.", enable_reasoning=True):
        full_prompt = self._maybe_add_reasoning_tag(prompt, enable_reasoning)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": full_prompt},
            ]},
        ]
        return self._call(messages)

    def reason_about_frames(self, frame_paths, prompt, system_prompt="You are a helpful robot reasoning assistant.", enable_reasoning=True):
        full_prompt = self._maybe_add_reasoning_tag(prompt, enable_reasoning)
        content = []
        for path in frame_paths:
            b64 = encode_image_to_base64(path)
            media_type = get_media_type(path)
            data_uri = f"data:{media_type};base64,{b64}"
            content.append({"type": "image_url", "image_url": {"url": data_uri}})
        content.append({"type": "text", "text": full_prompt})
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]
        return self._call(messages)

    def _call(self, messages):
        response = self.client.chat.completions.create(
            model=self.config.cosmos_model,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            stream=False,
        )
        raw_text = response.choices[0].message.content or ""
        usage = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
        }
        reasoning, answer = self._parse_reasoning(raw_text)
        return {"reasoning": reasoning, "answer": answer, "raw": raw_text, "usage": usage}

    @staticmethod
    def _maybe_add_reasoning_tag(prompt, enable):
        if not enable:
            return prompt
        return (
            f"{prompt}\n\n"
            "Answer the question using the following format:\n"
            "<think>\nYour reasoning.\n</think>\n\n"
            "Write your final answer immediately after the </think> tag."
        )

    @staticmethod
    def _parse_reasoning(text):
        if "<think>" in text and "</think>" in text:
            start = text.index("<think>") + len("<think>")
            end = text.index("</think>")
            reasoning = text[start:end].strip()
            answer = text[end + len("</think>"):].strip()
            return reasoning, answer
        return "", text.strip()
EOF