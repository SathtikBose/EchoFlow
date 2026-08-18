from unittest.mock import patch

import pytest

from app.input.commands import CommandProcessor


@pytest.fixture
def command_processor() -> CommandProcessor:
    return CommandProcessor()


def test_command_processor_enter(command_processor: CommandProcessor) -> None:
    with patch.object(command_processor.keyboard, "tap") as mock_tap:
        # Match variations
        assert command_processor.process("Press enter") is True
        assert command_processor.process("press enter.") is True
        assert command_processor.process("  press enter!  ") is True

        assert mock_tap.call_count == 3
        # Should be called with Key.enter, but we just check it was called


def test_command_processor_undo(command_processor: CommandProcessor) -> None:
    with patch.object(command_processor.keyboard, "pressed") as mock_pressed:
        with patch.object(command_processor.keyboard, "tap") as mock_tap:
            assert command_processor.process("Undo") is True
            assert command_processor.process("undo that.") is True

            assert mock_pressed.call_count == 2
            assert mock_tap.call_count == 2


def test_command_processor_no_match(command_processor: CommandProcessor) -> None:
    with patch.object(command_processor.keyboard, "tap") as mock_tap:
        assert command_processor.process("Hello world") is False
        assert command_processor.process("Press the enter key") is False  # Not an exact match

        mock_tap.assert_not_called()
