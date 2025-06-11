from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.core.database import SessionDep
from src.core.security import create_access_token
from src.librarians.dao import librarian_dao
from src.librarians.deps import CurLibrarianDep
from src.librarians.schemas import SLibrarian, SLibrarianCreate, Token
from src.librarians.service import authenticate_librarian

router = APIRouter(prefix="/librarians", tags=["Librarians"])


@router.post("/register")
async def register(session: SessionDep, librarian: SLibrarianCreate):
    librarian = await librarian_dao.create(session, **librarian.model_dump())
    if librarian:
        return {"message": "Librarian registered successfully"}


@router.post("/login", response_model=Token)
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    librarian = await authenticate_librarian(
        session, form_data.username, form_data.password
    )
    if not librarian:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(librarian.id)})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/check", response_model=SLibrarian)
async def check(session: SessionDep, librarian: CurLibrarianDep):
    return librarian
