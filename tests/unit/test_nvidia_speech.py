from collections.abc import Generator
from unittest.mock import MagicMock, patch

import httpx
import pytest

from app.speech.nvidia import NvidiaSpeechProvider


@pytest.fixture
def mock_settings() -> Generator[MagicMock, None, None]:
    with patch("app.speech.nvidia.settings") as mock:
        mock.nvidia_api_key = "test_key"
        mock.nvidia_base_url = "https://test.api.nvidia.com"
        mock.nvidia_speech_model = "test_model"
        mock.nvidia_timeout = 5.0
        yield mock


@pytest.mark.asyncio
async def test_nvidia_speech_provider_success(mock_settings: MagicMock) -> None:
    provider = NvidiaSpeechProvider()
    audio_data = b"dummy_audio_bytes"

    # Mock the httpx response
    mock_response = MagicMock()
    mock_response.json.return_value = {"text": "Hello world"}
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.post", return_value=mock_response) as mock_post:
        transcript = await provider.transcribe(audio_data)

        assert transcript == "Hello world"
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        assert kwargs["headers"]["Authorization"] == "Bearer test_key"
        assert kwargs["data"]["model"] == "test_model"
        assert "file" in kwargs["files"]


@pytest.mark.asyncio
async def test_nvidia_speech_provider_missing_key() -> None:
    with patch("app.speech.nvidia.settings") as mock:
        mock.nvidia_api_key = ""
        provider = NvidiaSpeechProvider()

        with pytest.raises(ValueError, match="API key is not configured"):
            await provider.transcribe(b"data")


@pytest.mark.asyncio
async def test_nvidia_speech_provider_timeout(mock_settings: MagicMock) -> None:
    provider = NvidiaSpeechProvider()

    with patch("httpx.AsyncClient.post", side_effect=httpx.TimeoutException("Timeout")):
        with pytest.raises(Exception, match="timed out"):
            await provider.transcribe(b"data")
