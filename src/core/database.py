from datetime import datetime
from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings


@cache
def get_db_url() -> str:
    return f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


engine = create_async_engine(get_db_url())
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=datetime.now
    )


async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise


SessionDep = Annotated[AsyncSession, Depends(get_db)]
