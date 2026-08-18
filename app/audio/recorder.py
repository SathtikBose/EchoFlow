import io
import logging
from typing import Any

import numpy as np
import sounddevice as sd
import soundfile as sf
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class AudioRecorder(QObject):
    # Signal emitted when recording is stopped and audio is ready.
    # Passes the audio data as bytes (WAV format).
    audio_ready = Signal(bytes)

    # Signal for errors
    error_occurred = Signal(str)

    def __init__(self, sample_rate: int = 16000, channels: int = 1) -> None:
        super().__init__()
        self.sample_rate = sample_rate
        self.channels = channels

        self.is_recording = False
        self._stream: sd.InputStream | None = None
        self._buffer: list[np.ndarray[Any, Any]] = []

    def get_devices(self) -> list[dict[str, Any]]:
        """List available input devices."""
        try:
            devices = sd.query_devices()
            return [d for d in devices if d['max_input_channels'] > 0]
        except Exception as e:
            logger.error(f"Failed to list devices: {e}")
            return []

    def start_recording(self, device_id: int | None = None) -> None:
        """Start capturing audio to a memory buffer."""
        if self.is_recording:
            return

        self._buffer.clear()

        try:
            # We use a callback to capture audio in a non-blocking way
            def callback(
                indata: np.ndarray[Any, Any], frames: int, time: Any, status: sd.CallbackFlags
            ) -> None:
                if status:
                    logger.warning(f"Audio callback status: {status}")
                self._buffer.append(indata.copy())

            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                device=device_id,
                callback=callback,
            )
            self._stream.start()
            self.is_recording = True
            logger.info("Microphone recording started.")
        except Exception as e:
            self.is_recording = False
            logger.error(f"Failed to start recording: {e}")
            self.error_occurred.emit(str(e))

    def stop_recording(self) -> None:
        """Stop capturing and emit the audio data."""
        if not self.is_recording or self._stream is None:
            return

        self.is_recording = False

        try:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            logger.info("Microphone recording stopped.")

            self._process_buffer()
        except Exception as e:
            logger.error(f"Failed to stop recording cleanly: {e}")
            self.error_occurred.emit(str(e))

    def _process_buffer(self) -> None:
        """Process the numpy buffer into a WAV byte stream."""
        if not self._buffer:
            logger.warning("Recording stopped but buffer is empty.")
            return

        # Concatenate all numpy arrays
        audio_data = np.concatenate(self._buffer, axis=0)
        self._buffer.clear()

        # Write to in-memory bytes buffer
        with io.BytesIO() as wav_io:
            sf.write(wav_io, audio_data, self.sample_rate, format="WAV", subtype="PCM_16")
            wav_bytes = wav_io.getvalue()

        logger.info(f"Generated {len(wav_bytes)} bytes of audio data.")
        self.audio_ready.emit(wav_bytes)
