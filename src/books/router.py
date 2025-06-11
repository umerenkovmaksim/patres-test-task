from fastapi import APIRouter, status

from src.books.dao import book_dao
from src.books.schemas import SBook, SBookCreate, SBookUpdate
from src.core.database import SessionDep
from src.librarians.deps import CurLibrarianDep

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=list[SBook])
async def get_books(session: SessionDep, librarian: CurLibrarianDep):
    return await book_dao.get(session)


@router.get("/{id}", response_model=SBook)
async def get_book(session: SessionDep, librarian: CurLibrarianDep, id: int):
    return await book_dao.get_by_id(session, id)


@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def create_book(
    session: SessionDep, librarian: CurLibrarianDep, book: SBookCreate
):
    return await book_dao.create(session, **book.model_dump())


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def put_book(
    session: SessionDep, librarian: CurLibrarianDep, book: SBookCreate, id: int
):
    await book_dao.update(session, id, **book.model_dump())


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def patch_book(
    session: SessionDep, librarian: CurLibrarianDep, book: SBookUpdate, id: int
):
    await book_dao.update(session, id, **book.model_dump(exclude_none=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(session: SessionDep, librarian: CurLibrarianDep, id: int):
    await book_dao.delete(session, id)
