import logging

import httpx

from app.core.config import settings
from app.speech.base import SpeechProvider

logger = logging.getLogger(__name__)


class NvidiaSpeechProvider(SpeechProvider):
    def __init__(self) -> None:
        self.api_key = settings.nvidia_api_key
        self.base_url = settings.nvidia_base_url
        self.model = settings.nvidia_speech_model
        self.timeout = settings.nvidia_timeout

    async def transcribe(self, audio_data: bytes) -> str:
        if not self.api_key:
            raise ValueError("NVIDIA API key is not configured.")

        endpoint = f"{self.base_url.rstrip('/')}/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

        # httpx multipart requires: files={'file': ('filename', file_obj, 'content_type')}
        files = {"file": ("audio.wav", audio_data, "audio/wav")}
        data = {"model": self.model, "response_format": "json"}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(
                    f"Sending {len(audio_data)} bytes to {endpoint} using model {self.model}"
                )
                response = await client.post(endpoint, headers=headers, files=files, data=data)
                response.raise_for_status()

                result = response.json()
                transcript = str(result.get("text", ""))

                logger.info(f"Transcription successful. Length: {len(transcript)} chars.")
                return transcript

        except httpx.TimeoutException as e:
            logger.error(f"NVIDIA API timeout: {e}")
            raise Exception("Transcription service timed out. Please try again.") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"NVIDIA API HTTP error {e.response.status_code}: {e.response.text}")
            raise Exception(f"Transcription service error: {e.response.status_code}") from e
        except Exception as e:
            logger.error(f"Unexpected error during transcription: {e}")
            raise Exception(f"Transcription failed: {str(e)}") from e
