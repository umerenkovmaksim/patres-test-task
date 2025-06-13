from fastapi import APIRouter, status

from src.books.dao import book_dao
from src.books.schemas import (
    BorrowBook,
    BorrowedBook,
    ReturnBook,
    SBook,
    SBookCreate,
    SBookUpdate,
)
from src.books.service import BookService
from src.core.database import SessionDep
from src.librarians.deps import CurLibrarianDep

router = APIRouter(tags=["Books"])


@router.get("/books", response_model=list[SBook])
async def get_books(session: SessionDep):
    return await book_dao.get(session)


@router.get("/books/{id}", response_model=SBook)
async def get_book(session: SessionDep, librarian: CurLibrarianDep, id: int):
    return await book_dao.get_by_id(session, id)


@router.post("/books", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def create_book(
    session: SessionDep, librarian: CurLibrarianDep, book: SBookCreate
):
    return await book_dao.create(session, **book.model_dump())


@router.put("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def put_book(
    session: SessionDep, librarian: CurLibrarianDep, book: SBookCreate, id: int
):
    await book_dao.update(session, id, **book.model_dump())


@router.patch("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def patch_book(
    session: SessionDep, librarian: CurLibrarianDep, book: SBookUpdate, id: int
):
    await book_dao.update(session, id, **book.model_dump(exclude_none=True))


@router.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(session: SessionDep, librarian: CurLibrarianDep, id: int):
    await book_dao.delete(session, id)


@router.post(
    "/borrow", response_model=BorrowedBook, status_code=status.HTTP_201_CREATED
)
async def borrow_book(
    session: SessionDep,
    librarian: CurLibrarianDep,
    borrow_data: BorrowBook,
):
    return await BookService.borrow_book(
        session, **borrow_data.model_dump(exclude_none=True)
    )


@router.post("/return", status_code=status.HTTP_204_NO_CONTENT)
async def return_book(
    session: SessionDep,
    librarian: CurLibrarianDep,
    return_data: ReturnBook,
):
    await BookService.return_book(session, **return_data.model_dump(exclude_none=True))
