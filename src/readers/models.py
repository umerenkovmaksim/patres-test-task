from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base, int_pk


class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int_pk]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
