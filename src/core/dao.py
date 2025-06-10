from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import Base

Model = TypeVar("Model", bound=Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model]) -> None:
        self.model = model

    async def get(self, session: AsyncSession, **filters: Any) -> list[Model]:
        query = select(self.model).filter_by(**filters)
        result = await session.execute(query)

        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, id: int) -> Model | None:
        result = await session.execute(select(self.model).filter_by(id=id))

        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, **kwargs: Any) -> Model:
        obj = self.model(**kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

        return obj

    async def update(
        self, session: AsyncSession, id: int, **kwargs: Any
    ) -> Model | None:
        result = await session.execute(select(self.model).filter_by(id=id))
        obj = result.scalars().first()
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await session.commit()
        await session.refresh(obj)

        return obj

    async def delete(self, session: AsyncSession, id: int) -> bool:
        result = await session.execute(select(self.model).filter_by(id=id))
        obj = result.scalars().first()

        if not obj:
            return False

        await session.delete(obj)
        await session.commit()

        return True
