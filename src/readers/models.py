from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, int_pk

if TYPE_CHECKING:
    from src.books.models import BorrowedBook


class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int_pk]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    borrowed_books: Mapped[list["BorrowedBook"]] = relationship(
        back_populates="reader", cascade="all, delete-orphan"
    )
