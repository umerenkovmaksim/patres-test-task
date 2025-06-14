import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.models import Book
from src.core.security import create_access_token
from src.librarians.models import Librarian
from src.readers.models import Reader


@pytest_asyncio.fixture
async def test_book(session: AsyncSession):
    book = Book(
        name="Test Book",
        author="Test Author",
        description="Test Description",
        year=2024,
        isbn="1234567890",
        copies=3,
    )
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


@pytest_asyncio.fixture
async def test_reader(session: AsyncSession):
    reader = Reader(name="Test Reader", email="test@example.com")
    session.add(reader)
    await session.commit()
    await session.refresh(reader)
    return reader


@pytest_asyncio.fixture
async def test_librarian(session: AsyncSession):
    librarian = Librarian(
        email="librarian@example.com", hashed_password="hashed_password"
    )
    session.add(librarian)
    await session.commit()
    await session.refresh(librarian)
    return librarian


@pytest_asyncio.fixture
def auth_token(test_librarian: Librarian):
    return create_access_token({"sub": str(test_librarian.id)})
