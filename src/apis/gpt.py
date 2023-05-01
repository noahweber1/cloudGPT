import os
from time import sleep
from typing import List, Tuple

import openai
from openai.error import RateLimitError, Timeout

from src.constants import (
    PRICING_GPT4_PROMPT,
    PRICING_GPT4_GENERATION,
    PRICING_GPT3_5_TURBO_PROMPT,
    PRICING_GPT3_5_TURBO_GENERATION,
)
from src.options.generate.prompt_system import (
    system_base_definition,
    executor_example,
    docarray_example,
    client_example,
)
from src.utils.io import timeout_generator_wrapper, GenerationTimeoutError
from src.utils.string_tools import print_colored


class AIModelSession:
    """A class to manage an AI model session."""

    def __init__(self, model: str = "gpt-4"):
        self.set_openai_api_key()
        if model == "gpt-4" and self.is_gpt4_supported():
            self.active_model = "gpt-4"
            self.prompt_cost = PRICING_GPT4_PROMPT
            self.generation_cost = PRICING_GPT4_GENERATION
        else:
            if model == "gpt-4":
                print_colored(
                    "GPT-4 is not available. Using GPT-3.5-turbo instead.", "yellow"
                )
                model = "gpt-3.5-turbo"
            self.active_model = model
            self.prompt_cost = PRICING_GPT3_5_TURBO_PROMPT
            self.generation_cost = PRICING_GPT3_5_TURBO_GENERATION
        self.total_prompt_chars = 0
        self.total_generation_chars = 0

    def set_openai_api_key(self):
        """Set the OpenAI API key."""
        if "OPENAI_API_KEY" not in os.environ:
            raise Exception(
                """
You need to set OPENAI_API_KEY in your environment.
If you have updated it already, please restart your terminal.
"""
            )
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def is_gpt4_supported(self):
        """Check if GPT-4 is available."""
        try:
            for _ in range(5):
                try:
                    openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "system", "content": "you respond nothing"}],
                    )
                    break
                except RateLimitError:
                    sleep(1)
                    continue
            return True
        except openai.error.InvalidRequestError:
            return False

    def calculate_cost(self, prompt_chars, generation_chars):
        """Calculate the cost based on characters in prompt and generation."""
        self.total_prompt_chars += prompt_chars
        self.total_generation_chars += generation_chars
        print("\n")
        prompt_expense = round(
            self.total_prompt_chars / 3.4 * self.prompt_cost / 1000, 3
        )
        generation_expense = round(
            self.total_generation_chars / 3.4 * self.generation_cost / 1000, 3
        )
        print("Estimated costs on openai.com:")
        print("total money spent so far:", f"${prompt_expense + generation_expense}")
        print("\n")

    def initiate_conversation(self, example_types: List[str] = ["executor", "docarray", "client"]):
        """Start a new conversation with the AI model."""
        return _AIModelConversation(self.active_model, self.calculate_cost, example_types)


class _AIModelConversation:
    """A class to manage an AI model conversation."""

    def __init__(
        self, model:
