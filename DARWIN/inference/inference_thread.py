#
#
import logging
from time import sleep

from camel.models import BaseModelBackend, ModelFactory
from camel.types import ModelPlatformType

from DARWIN.inference.anthropic_backend import AnthropicModelBackend
from DARWIN.inference.deepseek_backend import DeepSeekModelBackend

thread_log = logging.getLogger(name="inference.thread")
thread_log.setLevel("DEBUG")


class SharedMemory:
    Message_ID = 0
    Message = None
    Response = None
    Busy = False
    Working = False
    Done = False


class InferenceThread:

    def __init__(
        self,
        model_path:
        str = "/mnt/hwfile/trustai/models/Meta-Llama-3-8B-Instruct",  # noqa
        server_url: str = "http://10.140.0.144:8000/v1",
        stop_tokens: list[str] = None,
        model_platform_type: ModelPlatformType = ModelPlatformType.VLLM,
        model_type: str = "llama-3",
        temperature: float = 0.5,
        shared_memory: SharedMemory = None,
    ):
        self.alive = True
        self.count = 0
        self.server_url = server_url
        self.model_type = model_type

        # Register Anthropic backend
        if not hasattr(ModelPlatformType, "ANTHROPIC"):
            ModelPlatformType.ANTHROPIC = "anthropic"
        if not hasattr(ModelFactory, "_model_backend_mapping"):
            ModelFactory._model_backend_mapping = {}
        ModelFactory._model_backend_mapping[ModelPlatformType.ANTHROPIC] = AnthropicModelBackend

        # Register DeepSeek backend
        if not hasattr(ModelPlatformType, "DEEPSEEK"):
            ModelPlatformType.DEEPSEEK = "deepseek"
        ModelFactory._model_backend_mapping[ModelPlatformType.DEEPSEEK] = DeepSeekModelBackend

        # Determine model platform type
        if model_type.startswith("claude"):
            model_platform_type = ModelPlatformType.ANTHROPIC
        elif model_type.startswith("deepseek"):
            model_platform_type = ModelPlatformType.DEEPSEEK

        print("self.model_type:", self.model_type)
        self.model_backend: BaseModelBackend = ModelFactory.create(
            model_platform=model_platform_type,
            model_type=self.model_type,
            model_config_dict={
                "temperature": temperature,
                "stop": stop_tokens
            },
            url="vllm",
            api_key=server_url,
        )

        if shared_memory is None:
            self.shared_memory = SharedMemory()
        else:
            self.shared_memory = shared_memory

    def run(self):
        while self.alive:
            if self.shared_memory.Busy and not self.shared_memory.Working:
                self.shared_memory.Working = True
                try:
                    response = self.model_backend.run(
                        self.shared_memory.Message)
                    self.shared_memory.Response = response.choices[
                        0].message.content
                except Exception as e:
                    print("Receive Response Exception:", str(e))
                    self.shared_memory.Response = "No response."
                self.shared_memory.Done = True
                self.count += 1
                thread_log.info(
                    f"Thread {self.server_url}: {self.count} finished.")

            sleep(0.01)
