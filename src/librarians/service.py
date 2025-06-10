from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import verify_password
from src.librarians.dao import librarian_dao
from src.librarians.models import Librarian


async def authenticate_librarian(
    session: AsyncSession, email: str, password: str
) -> Librarian | None:
    librarian = await librarian_dao.get_by_email(session, email)
    if not librarian or not verify_password(password, librarian.password):
        return None
    return librarian
