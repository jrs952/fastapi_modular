# fastapi.quickstart/services/azure_openai_service.py

import os
import asyncio
from typing import Optional, List, Dict, Any
from ..config import Config
from .logging_service import LoggingService
import openai

class AzureOpenAIService:
    """
    Service to interact with Azure OpenAI API using the OpenAI Python library.
    """

    def __init__(self):
        self.logger = LoggingService.get_logger(self.__class__.__name__)
        service_config = Config.get_service_config("azure_openai")

        self.api_type = "azure"
        self.api_base = service_config.get("endpoint")  # Azure OpenAI endpoint
        self.api_key = service_config.get("api_key")
        self.api_version = service_config.get("api_version", "2023-05-15")  # Default version
        self.deployment_name = service_config.get("deployment_name")  # Deployment name

        if not all([self.api_base, self.api_key, self.deployment_name]):
            self.logger.error("Azure OpenAI configuration is missing.")
            raise ValueError("Azure OpenAI configuration is missing.")

        # Set the OpenAI library's configuration for Azure
        openai.api_type = self.api_type
        openai.api_base = self.api_base
        openai.api_version = self.api_version
        openai.api_key = self.api_key

        self.logger.info("Azure OpenAI client initialized using OpenAI Python library.")

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 100,
        temperature: float = 0.7,
        n: int = 1,
        stop: Optional[str] = None
    ) -> str:
        """
        Generate text using Azure OpenAI API.

        :param prompt: The prompt text to generate completion for.
        :param max_tokens: Maximum number of tokens to generate.
        :param temperature: Sampling temperature.
        :param n: Number of completions to generate.
        :param stop: Sequence where the API will stop generating further tokens.
        :return: Generated text.
        """
        self.logger.debug(f"Generating text with prompt: {prompt}")
        try:
            response = await asyncio.to_thread(
                openai.Completion.create,
                engine=self.deployment_name,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                n=n,
                stop=stop
            )
            generated_text = response.choices[0].text.strip()
            self.logger.debug(f"Generated text: {generated_text}")
            return generated_text
        except Exception as e:
            self.logger.error(f"Error generating text: {e}")
            raise

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text using Azure OpenAI API.

        :param text: The text to generate an embedding for.
        :return: The embedding vector as a list of floats.
        """
        self.logger.debug(f"Generating embedding for text: {text}")
        try:
            response = await asyncio.to_thread(
                openai.Embedding.create,
                engine=self.deployment_name,
                input=text
            )
            embedding = response['data'][0]['embedding']
            self.logger.debug(f"Generated embedding (first 5 values): {embedding[:5]}...")
            return embedding
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            raise

    async def generate_text_from_prompt(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Azure OpenAI API with a custom prompt.

        :param prompt: The prompt text to generate completion for.
        :param kwargs: Additional parameters for the completion.
        :return: The generated text.
        """
        self.logger.debug(f"Generating text from custom prompt.")
        try:
            response = await asyncio.to_thread(
                openai.Completion.create,
                engine=self.deployment_name,
                prompt=prompt,
                **kwargs
            )
            generated_text = response.choices[0].text.strip()
            self.logger.debug(f"Generated text: {generated_text}")
            return generated_text
        except Exception as e:
            self.logger.error(f"Error generating text from prompt: {e}")
            raise

def register_service():
    service_name = "azure_openai_service"
    service_class = AzureOpenAIService
    return service_name, service_class
