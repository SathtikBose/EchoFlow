import logging
from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select

logger = logging.getLogger(__name__)


class TranscriptionRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    original_text: str
    final_text: str
    mode: str
    inserted: bool = Field(default=False)


class HistoryDB:
    def __init__(self, db_path: str = "sqlite:///history.db") -> None:
        self.engine = create_engine(db_path, echo=False)
        SQLModel.metadata.create_all(self.engine)

    def add_record(
        self, original: str, final: str, mode: str, inserted: bool = True
    ) -> TranscriptionRecord:
        record = TranscriptionRecord(
            original_text=original, final_text=final, mode=mode, inserted=inserted
        )
        try:
            with Session(self.engine) as session:
                session.add(record)
                session.commit()
                session.refresh(record)
                return record
        except Exception as e:
            logger.error(f"Failed to add history record: {e}")
            raise

    def get_recent_records(self, limit: int = 50) -> list[TranscriptionRecord]:
        from sqlmodel import col

        with Session(self.engine) as session:
            statement = (
                select(TranscriptionRecord)
                .order_by(col(TranscriptionRecord.timestamp).desc())
                .limit(limit)
            )
            results = session.exec(statement).all()
            return list(results)
