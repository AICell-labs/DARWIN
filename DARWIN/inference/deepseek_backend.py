from typing import Any, Dict, List, Optional

import requests
from camel.models import BaseModelBackend
from camel.types import ModelType


class DeepSeekModelBackend(BaseModelBackend):
    """DeepSeek model backend."""

    def __init__(
        self,
        model_type: ModelType,
        model_config_dict: Dict[str, Any],
        url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        """Initialize the DeepSeek model backend.

        Args:
            model_type: The type of the model.
            model_config_dict: The configuration dictionary for the model.
            url: The URL of the API endpoint.
            api_key: The API key for authentication.
        """
        super().__init__(model_type, model_config_dict)
        self._url = url or "https://api.deepseek.com/v1"
        self._api_key = api_key
        self._model_name = self._get_model_name(model_type)

    def _get_model_name(self, model_type: ModelType) -> str:
        """Get the model name for the DeepSeek API.

        Args:
            model_type: The type of the model.

        Returns:
            The model name for the DeepSeek API.
        """
        model_name_mapping = {
            ModelType.DEEPSEEK_CODER: "deepseek-coder-33b-instruct",
            ModelType.DEEPSEEK_CHAT: "deepseek-chat-67b",
            ModelType.DEEPSEEK_MoE: "deepseek-moe-16b-chat",
        }
        return model_name_mapping.get(model_type, "deepseek-chat-67b")

    def run(self, messages: List[Dict[str, str]]) -> Any:
        """Run the model with the given messages.

        Args:
            messages: The list of messages to process.

        Returns:
            The model's response.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json"
            }

            # Convert messages to DeepSeek format
            deepseek_messages = []
            for message in messages:
                if message["role"] == "system":
                    deepseek_messages.append({
                        "role": "system",
                        "content": message["content"]
                    })
                else:
                    deepseek_messages.append({
                        "role": "user" if message["role"] == "user" else "assistant",
                        "content": message["content"]
                    })

            data = {
                "model": self._model_name,
                "messages": deepseek_messages,
                "temperature": self._model_config_dict.get("temperature", 0.7),
                "max_tokens": self._model_config_dict.get("max_tokens", 1024),
                "stream": False
            }

            response = requests.post(
                f"{self._url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()

            # Convert DeepSeek response to OpenAI format
            return type("Response", (), {
                "choices": [{
                    "message": {
                        "content": result["choices"][0]["message"]["content"],
                        "role": "assistant"
                    }
                }]
            })

        except Exception as e:
            raise Exception(f"Error running DeepSeek model: {str(e)}") 