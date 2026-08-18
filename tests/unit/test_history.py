import pytest

from app.db.history import HistoryDB


@pytest.fixture
def history_db() -> HistoryDB:
    # Use in-memory SQLite database for testing
    return HistoryDB("sqlite:///:memory:")


def test_history_add_record(history_db: HistoryDB) -> None:
    record = history_db.add_record(original="hello", final="Hello.", mode="default", inserted=True)

    assert record.id is not None
    assert record.original_text == "hello"
    assert record.final_text == "Hello."
    assert record.mode == "default"
    assert record.inserted is True


def test_history_get_recent(history_db: HistoryDB) -> None:
    history_db.add_record("first", "First.", "default", True)
    history_db.add_record("second", "Second.", "default", True)

    records = history_db.get_recent_records(limit=10)
    assert len(records) == 2
    # Ordered by timestamp desc, so second is first
    assert records[0].original_text == "second"
    assert records[1].original_text == "first"
