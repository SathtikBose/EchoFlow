import abc


class SpeechProvider(abc.ABC):
    """Base interface for all speech-to-text providers."""

    @abc.abstractmethod
    async def transcribe(self, audio_data: bytes) -> str:
        """
        Transcribes audio data (WAV bytes) into text.

        Args:
            audio_data: The audio data in WAV format.

        Returns:
            The transcribed text.

        Raises:
            Exception: If transcription fails.
        """
        pass
