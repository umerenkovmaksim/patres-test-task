from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, int_pk

if TYPE_CHECKING:
    from src.readers.models import Reader


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int_pk]
    name: Mapped[str]
    author: Mapped[str]
    description: Mapped[str | None]
    year: Mapped[int | None]
    isbn: Mapped[str | None] = mapped_column(unique=True)
    copies: Mapped[int] = mapped_column(default=1)

    borrowed_books: Mapped[list["BorrowedBook"]] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )

    __table_args__ = (CheckConstraint("copies >= 0", name="check_copies_count"),)


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int_pk]
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    borrow_date: Mapped[datetime] = mapped_column(default=datetime.now())
    return_date: Mapped[datetime | None]

    book: Mapped["Book"] = relationship("Book", back_populates="borrowed_books")
    reader: Mapped["Reader"] = relationship("Reader", back_populates="borrowed_books")
