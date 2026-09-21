from abc import ABC, abstractmethod
# pyrefly: ignore [missing-import]
import ollama
# pyrefly: ignore [missing-import]
from app.core.config import settings

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    Any new provider should inherit from this class and implement the generate method.
    """
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response given a prompt.
        
        Args:
            prompt (str): The input text to prompt the LLM.
            
        Returns:
            str: The generated text response.
        """
        pass


class OllamaProvider(LLMProvider):
    """
    Ollama implementation of the LLM provider.
    Reads the host and model configuration from the settings module.
    """
    
    def __init__(self):
        # Initialize the Ollama client with the host from settings
        self.client = ollama.Client(host=settings.ollama_host)
        self.model = settings.llm_model

    def generate(self, prompt: str) -> str:
        # Use the configured model to generate a response
        response = self.client.generate(model=self.model, prompt=prompt)
        return response['response']


def get_llm_provider(provider_name: str = "ollama") -> LLMProvider:
    """
    Factory function to get an instance of an LLM provider.
    This allows adding new providers in the future without changing the agent's code.
    
    Args:
        provider_name (str): The name of the provider to instantiate.
        
    Returns:
        LLMProvider: An instance of the requested LLM provider.
    """
    providers = {
        "ollama": OllamaProvider,
        # Additional providers can be added here in the future
        # e.g., "openai": OpenAIProvider,
    }
    
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
        
    return provider_class()
