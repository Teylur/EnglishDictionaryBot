from typing import List

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON

class WordORM(Base):
    __tablename__ = "words"

    body: Mapped[str]
    user_id: Mapped[str | None]
    translate: Mapped[str | None]
    examples: Mapped[List[str] | None] = mapped_column(JSON)
