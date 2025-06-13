from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.dao import book_dao, borrowed_book_dao
from src.books.models import BorrowedBook
from src.readers.dao import reader_dao


class BookService:
    @classmethod
    async def borrow_book(
        cls,
        session: AsyncSession,
        book_id: int,
        reader_id: int,
        borrow_date: datetime | None = datetime.now(),
    ) -> BorrowedBook:
        book = await book_dao.get_by_id(session, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Книга не найдена",
            )
        if book.copies <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нет доступных копий книги",
            )

        reader = await reader_dao.get_by_id(session, reader_id)

        if not reader:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Читатель не найден",
            )

        borrowed_books = await borrowed_book_dao.get(session, reader_id=reader.id)
        active_borrows = [b for b in borrowed_books if b.return_date is None]
        if len(active_borrows) >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Превышен лимит активных выдач",
            )

        borrow = await borrowed_book_dao.create(
            session,
            book_id=book_id,
            reader_id=reader_id,
            borrow_date=borrow_date,
        )

        await book_dao.update(session, book_id, copies=book.copies - 1)

        return borrow

    @classmethod
    async def return_book(
        cls,
        session: AsyncSession,
        borrow_id: int,
        return_date: datetime | None = datetime.now(),
    ) -> BorrowedBook:
        borrow = await borrowed_book_dao.get_by_id(session, borrow_id)
        if not borrow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запись о выдаче не найдена",
            )

        if borrow.return_date is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Книга уже возвращена",
            )

        book = await book_dao.get_by_id(session, borrow.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Книга не найдена",
            )

        borrow = await borrowed_book_dao.update(
            session,
            borrow.id,
            return_date=return_date,
        )

        await book_dao.update(session, book.id, copies=book.copies + 1)

        return borrow

    @classmethod
    async def get_reader_books(
        cls,
        session: AsyncSession,
        reader_id: int,
    ) -> list[BorrowedBook]:
        reader = await reader_dao.get_by_id(session, reader_id)
        if not reader:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Читатель не найден",
            )

        return await borrowed_book_dao.get(
            session, reader_id=reader_id, return_date=None
        )
