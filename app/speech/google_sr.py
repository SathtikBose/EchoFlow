import asyncio
import io
import logging

import speech_recognition as sr

from app.speech.base import SpeechProvider

logger = logging.getLogger(__name__)


class GoogleSpeechProvider(SpeechProvider):
    """
    A SpeechProvider that uses the SpeechRecognition library's
    built-in Google Web Speech API for fast, free, and robust
    offline-ish (sends to Google) transcription.
    """

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    async def transcribe(self, audio_data: bytes) -> str:
        if not audio_data:
            return ""

        logger.info(f"Preparing to transcribe {len(audio_data)} bytes using SpeechRecognition.")

        # SpeechRecognition expects a file-like object containing WAV data
        with io.BytesIO(audio_data) as wav_io:
            try:
                # Load the audio data
                with sr.AudioFile(wav_io) as source:
                    audio = self.recognizer.record(source)

                # We run this in an executor so it doesn't block the async loop
                # though TranscriptionService already runs in a separate QThread,
                # we maintain async correctness here.
                loop = asyncio.get_running_loop()

                logger.info("Sending audio to Google Web Speech API...")
                transcript = await loop.run_in_executor(
                    None, self.recognizer.recognize_google, audio
                )

                # Make sure it's a string
                transcript = str(transcript)

                logger.info(f"Transcription successful. Length: {len(transcript)} chars.")
                return transcript

            except sr.UnknownValueError:
                logger.warning("SpeechRecognition could not understand the audio.")
                return ""  # Return empty if it was just noise
            except sr.RequestError as e:
                logger.exception("Could not request results from Google Web Speech API")
                raise Exception(f"Transcription service error: {e}") from e
            except Exception as e:
                logger.exception("Unexpected error during transcription")
                raise Exception(f"Transcription failed: {repr(e)}") from e
