import abc


class LlmProvider(abc.ABC):
    """Base interface for all LLM providers."""

    @abc.abstractmethod
    async def transform_text(
        self, text: str, mode: str = "default", app_context: str | None = None
    ) -> str:
        """
        Transforms text using an LLM based on the given mode and context.

        Args:
            text: The raw transcribed text.
            mode: The transformation mode (e.g., 'default', 'formal', 'casual').
            app_context: The title of the active window for context.

        Returns:
            The transformed text.

        Raises:
            Exception: If transformation fails.
        """
        pass
