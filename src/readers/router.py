from fastapi import APIRouter, status

from src.core.database import SessionDep
from src.librarians.deps import CurLibrarianDep
from src.readers.dao import reader_dao
from src.readers.schemas import SReader, SReaderCreate, SReaderUpdate

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.get("", response_model=list[SReader])
async def get_readers(session: SessionDep, librarian: CurLibrarianDep):
    return await reader_dao.get(session)


@router.get("/{id}", response_model=SReader)
async def get_reader(session: SessionDep, librarian: CurLibrarianDep, id: int):
    return await reader_dao.get_by_id(session, id)


@router.post("", response_model=SReader, status_code=status.HTTP_201_CREATED)
async def create_reader(
    session: SessionDep, librarian: CurLibrarianDep, book: SReaderCreate
):
    return await reader_dao.create(session, **book.model_dump())


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def put_reader(
    session: SessionDep, librarian: CurLibrarianDep, book: SReaderCreate, id: int
):
    await reader_dao.update(session, id, **book.model_dump())


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def patch_reader(
    session: SessionDep, librarian: CurLibrarianDep, book: SReaderUpdate, id: int
):
    await reader_dao.update(session, id, **book.model_dump(exclude_none=True))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reader(session: SessionDep, librarian: CurLibrarianDep, id: int):
    await reader_dao.delete(session, id)
