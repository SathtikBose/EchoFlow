import json
from pathlib import Path

import pytest

from app.input.dictionary import DictionaryProcessor


@pytest.fixture
def temp_dict_file(tmp_path: Path) -> Path:
    dict_file = tmp_path / "dictionary.json"
    return dict_file


def test_dictionary_processor_loads_defaults(temp_dict_file: Path) -> None:
    processor = DictionaryProcessor(str(temp_dict_file))
    assert "pedantic" in processor.mappings
    assert processor.mappings["pedantic"] == "Pydantic"

    # Process text
    result = processor.process("I am using pedantic for parsing.")
    assert result == "I am using Pydantic for parsing."


def test_dictionary_processor_custom_mappings(temp_dict_file: Path) -> None:
    # Pre-create file
    with open(temp_dict_file, "w", encoding="utf-8") as f:
        json.dump({"teh": "the", "hello world": "Hello World"}, f)

    processor = DictionaryProcessor(str(temp_dict_file))
    assert processor.process("teh cat") == "the cat"

    # Add mapping dynamically
    processor.add_mapping("tets", "test")
    assert processor.process("This is a tets") == "This is a test"

    # Ensure it's not doing partial word matches
    assert processor.process("tetsing") == "tetsing"
