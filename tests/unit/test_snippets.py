import json
from pathlib import Path

import pytest

from app.input.snippets import SnippetProcessor


@pytest.fixture
def temp_snippet_file(tmp_path: Path) -> Path:
    return tmp_path / "snippets.json"


def test_snippet_processor_loads_defaults(temp_snippet_file: Path) -> None:
    processor = SnippetProcessor(str(temp_snippet_file))
    assert "insert signature" in processor.snippets

    # Exact match triggers
    result = processor.process("insert signature")
    assert result is not None
    assert "Best regards" in result

    # Case insensitive match with punctuation
    result = processor.process("Insert signature!")
    assert result is not None
    assert "Best regards" in result


def test_snippet_processor_custom_snippets(temp_snippet_file: Path) -> None:
    # Pre-create file
    with open(temp_snippet_file, "w", encoding="utf-8") as f:
        json.dump({"address": "123 Main St, Anytown USA"}, f)

    processor = SnippetProcessor(str(temp_snippet_file))
    assert processor.process("address") == "123 Main St, Anytown USA"

    # Add mapping dynamically
    processor.add_snippet("my email", "test@example.com")
    assert processor.process("my email") == "test@example.com"

    # Partial match should return None
    assert processor.process("what is my email") is None
