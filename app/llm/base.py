import abc


class LlmProvider(abc.ABC):
    """Base interface for all LLM providers."""

    @abc.abstractmethod
    async def transform_text(self, text: str, mode: str = "default") -> str:
        """
        Transforms text using an LLM based on the given mode.

        Args:
            text: The raw transcribed text.
            mode: The transformation mode (e.g., 'default', 'formal', 'casual').

        Returns:
            The transformed text.

        Raises:
            Exception: If transformation fails.
        """
        pass
