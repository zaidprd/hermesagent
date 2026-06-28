from openai import OpenAI

from . import config


class AIGateway:
    """Single entry point for text generation across OpenAI-compatible
    providers (SumoPod, OpenAI, OpenRouter, local). Add a provider = change
    env config, not code."""

    def __init__(self, api_key=None, base_url=None, model=None):
        self.model = model or config.AI_TEXT_MODEL
        self.client = OpenAI(
            api_key=api_key or config.AI_API_KEY,
            base_url=base_url or config.AI_BASE_URL,
        )

    def generate_text(self, messages, model=None, **kwargs):
        resp = self.client.chat.completions.create(
            model=model or self.model,
            messages=messages,
            **kwargs,
        )
        return resp.choices[0].message.content or ""

    def generate_image(self, prompt, model=None, size="1024x1024"):
        """Generate an image and return its URL. Returns '' if no model configured."""
        image_model = model or config.AI_IMAGE_MODEL
        if not image_model:
            return ""
        resp = self.client.images.generate(
            model=image_model,
            prompt=prompt,
            n=1,
            size=size,
        )
        return (resp.data[0].url or "") if resp.data else ""
