import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SnippetProcessor:
    def __init__(self, config_path: str = "snippets.json") -> None:
        self.config_path = Path(config_path)
        self.snippets: dict[str, str] = {}
        self._load_snippets()

    def _load_snippets(self) -> None:
        if self.config_path.exists():
            try:
                with open(self.config_path, encoding="utf-8") as f:
                    self.snippets = json.load(f)
                logger.info(f"Loaded {len(self.snippets)} snippets.")
            except Exception as e:
                logger.error(f"Failed to load snippets: {e}")
                self.snippets = {}
        else:
            # Default example snippet
            self._save_snippets({"insert signature": "Best regards,\nJohn Doe\nSoftware Engineer"})

    def _save_snippets(self, snippets: dict[str, str]) -> None:
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(snippets, f, indent=4)
            self.snippets = snippets
        except Exception as e:
            logger.error(f"Failed to save snippets: {e}")

    def add_snippet(self, trigger: str, content: str) -> None:
        self.snippets[trigger.lower()] = content
        self._save_snippets(self.snippets)

    def process(self, text: str) -> str | None:
        """
        Checks if the text exactly matches a snippet trigger (ignoring case and punctuation).
        Returns the snippet content if matched, None otherwise.
        """
        if not text or not self.snippets:
            return None

        # Clean the text for matching
        clean_text = text.lower().strip()
        import re

        clean_text = re.sub(r"[.!?]+$", "", clean_text).strip()

        for trigger, content in self.snippets.items():
            if clean_text == trigger.lower():
                return content

        return None
