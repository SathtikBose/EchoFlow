from collections.abc import Generator
from unittest.mock import MagicMock, patch

import httpx
import pytest

from app.llm.nvidia import NvidiaLlmProvider


@pytest.fixture
def mock_settings() -> Generator[MagicMock, None, None]:
    with patch("app.llm.nvidia.settings") as mock:
        mock.nvidia_api_key = "test_key"
        mock.nvidia_base_url = "https://test.api.nvidia.com"
        mock.nvidia_llm_model = "test_model"
        mock.nvidia_timeout = 5.0
        yield mock


@pytest.mark.asyncio
async def test_nvidia_llm_provider_success(mock_settings: MagicMock) -> None:
    provider = NvidiaLlmProvider()
    input_text = "hello world"

    # Mock the httpx response
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": [{"message": {"content": "Hello, world!"}}]}
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.post", return_value=mock_response) as mock_post:
        transformed = await provider.transform_text(input_text)

        assert transformed == "Hello, world!"
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        assert kwargs["headers"]["Authorization"] == "Bearer test_key"
        assert kwargs["json"]["model"] == "test_model"
        assert len(kwargs["json"]["messages"]) == 2
        assert kwargs["json"]["messages"][1]["content"] == "hello world"


@pytest.mark.asyncio
async def test_nvidia_llm_provider_missing_key() -> None:
    with patch("app.llm.nvidia.settings") as mock:
        mock.nvidia_api_key = ""
        provider = NvidiaLlmProvider()

        with pytest.raises(ValueError, match="API key is not configured"):
            await provider.transform_text("test")


@pytest.mark.asyncio
async def test_nvidia_llm_provider_timeout(mock_settings: MagicMock) -> None:
    provider = NvidiaLlmProvider()

    with patch("httpx.AsyncClient.post", side_effect=httpx.TimeoutException("Timeout")):
        with pytest.raises(Exception, match="timed out"):
            await provider.transform_text("test")
