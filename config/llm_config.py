import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()


class LLMConfig:
    """
    Flexible configuration class for any LLM provider with DSPy.
    Supports Gemini, OpenAI, Anthropic, and other providers.
    """

    def __init__(self, provider: str = "gemini"):
        self.provider = provider.lower()
        self._setup_provider_config()

    def _setup_provider_config(self):
        """Setup configuration based on the selected provider."""

        if self.provider == "gemini":
            self._setup_gemini()
        elif self.provider == "openai":
            self._setup_openai()
        elif self.provider == "anthropic":
            self._setup_anthropic()

        else:
            raise ValueError(
                f"Unsupported LLM provider: {self.provider}. Supported providers: gemini, openai, anthropic, azure"
            )

    def _setup_gemini(self):
        """Configure for Google Gemini."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "8000"))
        self.temperature = float(os.getenv("GEMINI_TEMPERATURE", "0"))
        self.cache = os.getenv("GEMINI_CACHE", "true").lower() == "true"

        # DSPy format for Gemini
        self.dspy_model = f"gemini/{self.model_name}"

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required for Gemini provider"
            )

    def _setup_openai(self):
        """Configure for OpenAI."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4.1")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "16000"))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0"))
        self.cache = os.getenv("OPENAI_CACHE", "true").lower() == "true"

        # DSPy format for OpenAI
        self.dspy_model = f"openai/{self.model_name}"

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required for OpenAI provider"
            )

    def _setup_anthropic(self):
        """Configure for Anthropic Claude."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model_name = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        self.max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4000"))
        self.temperature = float(os.getenv("ANTHROPIC_TEMPERATURE", "0"))
        self.cache = os.getenv("ANTHROPIC_CACHE", "true").lower() == "true"

        # DSPy format for Anthropic
        self.dspy_model = f"anthropic/{self.model_name}"

        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required for Anthropic provider"
            )

    def get_dspy_config(self) -> Dict[str, Any]:
        """
        Get the configuration dictionary for DSPy LM initialization.

        Returns:
            Dict with configuration for dspy.LM()
        """
        config = {
            "model": self.dspy_model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "cache": self.cache,
        }

        # Add API key if required
        if self.api_key:
            config["api_key"] = self.api_key

        return config

    def create_dspy_lm(self):
        """
        Create and return a configured DSPy LM instance.

        Returns:
            dspy.LM: Configured language model instance
        """
        import dspy

        config = self.get_dspy_config()
        return dspy.LM(**config)

    def __str__(self):
        """String representation of the config."""
        return f"LLMConfig(provider={self.provider}, model={self.dspy_model}, max_tokens={self.max_tokens})"

    def __repr__(self):
        return self.__str__()


# Provider-specific convenience functions
def get_gemini_config():
    """Get Gemini configuration."""
    return LLMConfig(provider="gemini")


def get_openai_config():
    """Get OpenAI configuration."""
    return LLMConfig(provider="openai")


def get_anthropic_config():
    """Get Anthropic configuration."""
    return LLMConfig(provider="anthropic")


# Example usage and configuration validation
if __name__ == "__main__":
    # Test different providers
    providers = ["gemini", "openai", "anthropic"]

    for provider in providers:
        try:
            config = LLMConfig(provider=provider)
            print(f"✅ {provider.upper()}: {config}")
            print(f"   DSPy Config: {config.get_dspy_config()}")
            print()
        except ValueError as e:
            print(f"❌ {provider.upper()}: {e}")
            print()
