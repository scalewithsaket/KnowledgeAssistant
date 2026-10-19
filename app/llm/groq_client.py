"""
LLM client class for Groq API
"""
from groq import Groq
from app.core.config import settings

class GroqClient:
    """
    LLM client class for Groq API
    """
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Takes the system prompt, context, user query and using Groq API generates response.
        """
        completion = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=settings.llm_temperature,
            max_completion_tokens=settings.llm_max_completion_tokens,
            top_p=settings.llm_top_p,
            reasoning_effort=settings.llm_reasoning_effort,
            stream=settings.llm_stream,
        )
        return completion.choices[0].message.content
