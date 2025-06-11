from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base, int_pk


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int_pk]
    name: Mapped[str]
    author: Mapped[str]
    year: Mapped[int | None]
    isbn: Mapped[str | None] = mapped_column(unique=True)
    copies: Mapped[int] = mapped_column(default=1)

    __table_args__ = (CheckConstraint("copies >= 0", name="check_copies_count"),)
