from .backends import backend
from .dispatcher import Dispatcher, TrainTask
from .evaluator import EvaluateConfig, evaluate
from .generator import GenerateConfig, generate
from .model import LLMModel
from .modules import (
    AdapterConfig,
    LLMBatchConfig,
    LLMCache,
    LLMForCausalLM,
    LLMModelConfig,
    LLMModelInput,
    LLMModelOutput,
    LoraConfig,
    MixLoraConfig,
    cache_factory,
    lora_config_factory,
)
from .prompter import Prompter
from .tokenizer import Tokenizer
from .trainer import TrainConfig, train
from .utils import is_package_available, setup_logging

assert is_package_available("torch", "2.3.0"), "MoE-PEFT requires torch>=2.3.0"
assert is_package_available(
    "transformers", "4.43.0"
), "MoE-PEFT requires transformers>=4.43.0"

setup_logging()

__all__ = [
    "LLMCache",
    "cache_factory",
    "LLMModelConfig",
    "LLMModelOutput",
    "LLMForCausalLM",
    "LLMBatchConfig",
    "LLMModelInput",
    "AdapterConfig",
    "LoraConfig",
    "MixLoraConfig",
    "lora_config_factory",
    "TrainTask",
    "Dispatcher",
    "EvaluateConfig",
    "evaluate",
    "GenerateConfig",
    "generate",
    "TrainConfig",
    "train",
    "LLMModel",
    "Prompter",
    "Tokenizer",
    "setup_logging",
    "backend",
]
