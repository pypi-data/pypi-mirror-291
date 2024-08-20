from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, NonNegativeInt, PositiveFloat, PositiveInt


class FinetuningConfig(BaseModel):
    base_model: str
    adapter: str = Field(default="lora")
    task: str | None = Field(default=None)
    epochs: PositiveInt | None = Field(default=None)
    learning_rate: PositiveFloat | None = Field(default=None)
    rank: PositiveInt | None = Field(default=None)
    target_modules: list[str] | None = Field(default=None)
    enable_early_stopping: bool = Field(default=True)


class DeploymentConfig(BaseModel):
    base_model: str
    accelerator: str | None = Field(default=None)
    cooldown_time: PositiveInt | None = Field(default=43200)
    hf_token: str | None = Field(default=None)
    min_replicas: NonNegativeInt | None = Field(default=None)
    max_replicas: PositiveInt | None = Field(default=None)
    scale_up_threshold: PositiveInt | None = Field(default=None)


class AugmentationConfig(BaseModel):
    """Configuration for synthetic data generation tasks.

    # Attributes
    :param base_model: (str) The OpenAI model to prompt.
    :param num_samples_to_generate: (int) The number of synthetic examples to generate.
    :param num_seed_samples: (int) The number of seed samples to use for generating synthetic examples.
    :param task_context: (str) The user-provided task context for generating candidates.
    """

    base_model: str
    num_samples_to_generate: int = Field(default=1000)
    num_seed_samples: int | str = Field(default="all")
    augmentation_strategy: str = Field(default="mixture_of_agents")
    task_context: str = Field(default="")

    @field_validator("base_model")
    @classmethod
    def validate_base_model(cls, base_model) -> str:
        supoorted_base_models = {
            "gpt-4-turbo",
            "gpt-4-0125-preview",
            "gpt-4-1106-preview",
            "gpt-4o",
            "gpt-4o-2024-08-06",
            "gpt-4o-mini",
        }
        if base_model not in supoorted_base_models:
            raise ValueError(
                f"base_model must be one of {supoorted_base_models}.",
            )
        return base_model

    @field_validator("num_samples_to_generate")
    @classmethod
    def validate_num_samples_to_generate(cls, num_samples_to_generate) -> int:
        if num_samples_to_generate < 1:
            raise ValueError("num_samples_to_generate must be >= 1.")
        return num_samples_to_generate

    @field_validator("num_seed_samples")
    @classmethod
    def validate_num_seed_samples(cls, num_seed_samples):
        if isinstance(num_seed_samples, str) and num_seed_samples != "all":
            raise ValueError("num_seed_samples can only be an integer or the string 'all'.")
        elif isinstance(num_seed_samples, int) and num_seed_samples < 1:
            raise ValueError("num_seed_samples must be >= 1.")
        return num_seed_samples

    @field_validator("augmentation_strategy")
    @classmethod
    def validate_augmentation_strategy(cls, augmentation_strategy):
        if augmentation_strategy not in {"single_pass", "mixture_of_agents"}:
            raise ValueError("augmentation_strategy must be 'single_pass' or 'mixture_of_agents'.")
        return augmentation_strategy
