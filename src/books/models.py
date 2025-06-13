from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base, int_pk

if TYPE_CHECKING:
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int_pk]
    name: Mapped[str]
    author: Mapped[str]
    description: Mapped[str | None]
    year: Mapped[int | None]
    isbn: Mapped[str | None] = mapped_column(unique=True)
    copies: Mapped[int] = mapped_column(default=1)

    __table_args__ = (CheckConstraint("copies >= 0", name="check_copies_count"),)


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int_pk]
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    borrow_date: Mapped[datetime] = mapped_column(default=datetime.now())
    return_date: Mapped[datetime | None]
