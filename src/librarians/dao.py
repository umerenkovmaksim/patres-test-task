from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dao import BaseDAO
from src.core.security import hash_password
from src.librarians.models import Librarian


class LibrarianDAO(BaseDAO[Librarian]):
    def __init__(self) -> None:
        super().__init__(Librarian)

    async def create(self, session: AsyncSession, **kwargs) -> Librarian:
        kwargs["hashed_password"] = hash_password(kwargs["password"])
        del kwargs["password"]
        return await super().create(session, **kwargs)

    async def get_by_email(self, session: AsyncSession, email: str) -> Librarian | None:
        result = await self.get(session, email=email)
        if result:
            return result[0]
        return None


librarian_dao = LibrarianDAO()
