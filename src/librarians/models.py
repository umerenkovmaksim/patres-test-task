from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base, int_pk


class Librarian(Base):
    __tablename__ = "librarians"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
