import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class DictionaryProcessor:
    def __init__(self, config_path: str = "dictionary.json") -> None:
        self.config_path = Path(config_path)
        self.mappings: dict[str, str] = {}
        self._load_mappings()

    def _load_mappings(self) -> None:
        if self.config_path.exists():
            try:
                with open(self.config_path, encoding="utf-8") as f:
                    self.mappings = json.load(f)
                logger.info(f"Loaded {len(self.mappings)} dictionary mappings.")
            except Exception as e:
                logger.error(f"Failed to load dictionary: {e}")
                self.mappings = {}
        else:
            # Create a default empty one
            self._save_mappings({"pedantic": "Pydantic"})

    def _save_mappings(self, mappings: dict[str, str]) -> None:
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(mappings, f, indent=4)
            self.mappings = mappings
        except Exception as e:
            logger.error(f"Failed to save dictionary: {e}")

    def add_mapping(self, wrong_word: str, correct_word: str) -> None:
        self.mappings[wrong_word.lower()] = correct_word
        self._save_mappings(self.mappings)

    def process(self, text: str) -> str:
        """Applies dictionary replacements to the transcribed text."""
        if not text or not self.mappings:
            return text

        processed_text = text
        for wrong, right in self.mappings.items():
            # Use regex for word boundaries to avoid partial matches
            # e.g., mapping 'pedantic' to 'Pydantic'
            pattern = re.compile(rf"\b{re.escape(wrong)}\b", re.IGNORECASE)
            processed_text = pattern.sub(right, processed_text)

        return processed_text
