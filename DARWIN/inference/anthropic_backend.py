from typing import Any, Dict, List, Optional

import anthropic
from camel.models import BaseModelBackend
from camel.types import ModelType


class AnthropicModelBackend(BaseModelBackend):
    """Anthropic model backend."""

    def __init__(
        self,
        model_type: ModelType,
        model_config_dict: Dict[str, Any],
        url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        """Initialize the Anthropic model backend.

        Args:
            model_type: The type of the model.
            model_config_dict: The configuration dictionary for the model.
            url: The URL of the API endpoint.
            api_key: The API key for authentication.
        """
        super().__init__(model_type, model_config_dict)
        self._url = url
        self._api_key = api_key or anthropic.api_key
        self._client = anthropic.Anthropic(api_key=self._api_key)
        self._model_name = self._get_model_name(model_type)

    def _get_model_name(self, model_type: ModelType) -> str:
        """Get the model name for the Anthropic API.

        Args:
            model_type: The type of the model.

        Returns:
            The model name for the Anthropic API.
        """
        model_name_mapping = {
            ModelType.CLAUDE_3_OPUS: "claude-3-opus-20240229",
            ModelType.CLAUDE_3_SONNET: "claude-3-sonnet-20240229",
            ModelType.CLAUDE_3_HAIKU: "claude-3-haiku-20240307",
            ModelType.CLAUDE_2_1: "claude-2.1",
            ModelType.CLAUDE_2: "claude-2",
            ModelType.CLAUDE_INSTANT: "claude-instant-1.2",
        }
        return model_name_mapping.get(model_type, "claude-3-sonnet-20240229")

    def run(self, messages: List[Dict[str, str]]) -> Any:
        """Run the model with the given messages.

        Args:
            messages: The list of messages to process.

        Returns:
            The model's response.
        """
        try:
            # Convert OpenAI message format to Anthropic format
            system_message = None
            user_messages = []
            
            for message in messages:
                if message["role"] == "system":
                    system_message = message["content"]
                else:
                    user_messages.append({
                        "role": "user" if message["role"] == "user" else "assistant",
                        "content": message["content"]
                    })

            # Create the message for Anthropic API
            response = self._client.messages.create(
                model=self._model_name,
                system=system_message,
                messages=user_messages,
                temperature=self._model_config_dict.get("temperature", 0.7),
                max_tokens=self._model_config_dict.get("max_tokens", 1024),
            )

            # Convert Anthropic response to OpenAI format
            return type("Response", (), {
                "choices": [{
                    "message": {
                        "content": response.content[0].text,
                        "role": "assistant"
                    }
                }]
            })

        except Exception as e:
            raise Exception(f"Error running Anthropic model: {str(e)}") 