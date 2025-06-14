from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.models import Book, BorrowedBook
from src.books.service import BookService
from src.readers.models import Reader


@pytest.mark.asyncio
async def test_borrow_book_success(
    session: AsyncSession, test_book: Book, test_reader: Reader
):
    borrowed_book = await BookService.borrow_book(
        session=session, book_id=test_book.id, reader_id=test_reader.id
    )

    assert borrowed_book.book_id == test_book.id
    assert borrowed_book.reader_id == test_reader.id
    assert borrowed_book.return_date is None

    await session.refresh(test_book)
    assert test_book.copies == 2


@pytest.mark.asyncio
async def test_borrow_book_no_copies(
    session: AsyncSession, test_book: Book, test_reader: Reader
):
    test_book.copies = 0
    await session.commit()

    with pytest.raises(Exception) as exc_info:
        await BookService.borrow_book(
            session=session, book_id=test_book.id, reader_id=test_reader.id
        )

    assert "Нет доступных копий книги" in str(exc_info)


@pytest.mark.asyncio
async def test_borrow_book_limit_exceeded(
    session: AsyncSession, test_book: Book, test_reader: Reader
):
    for _ in range(3):
        borrowed = BorrowedBook(
            book_id=test_book.id, reader_id=test_reader.id, borrow_date=datetime.now()
        )
        session.add(borrowed)
    await session.commit()

    with pytest.raises(Exception) as exc:
        await BookService.borrow_book(
            session=session, book_id=test_book.id, reader_id=test_reader.id
        )

    assert "Превышен лимит активных выдач" in str(exc)
