import os
from openai import OpenAI
from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class LLMProvider:
    provider: str
    model: str

    @staticmethod
    def from_env_or_config(cfg: Dict[str, Any]) -> "LLMProvider":
        provider = os.getenv("LLM_PROVIDER") or "local"
        model = os.getenv("LLM_MODEL") or "deepseek-r1:8b"
        return LLMProvider(provider=provider, model=model)

    def complete(self, system: str, messages: List[Dict[str, str]], user: str, refusal_prompt: str, mode: str = "normal") -> str:
        if self.provider == "local":
            client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
            history = [{"role": "system", "content": system}]
            history.extend(messages)
            
            prompt = user if mode != "refusal" else f"{refusal_prompt}\n\nUser Request: {user}"
            history.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model,
                messages=history,
                temperature=float(os.getenv("LLM_TEMPERATURE", 0.6))
            )
            return response.choices[0].message.content
        return "Provider error: Check .env settings."