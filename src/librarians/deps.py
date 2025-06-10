from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import jwt
from jose.exceptions import JWTError

from src.core.config import settings
from src.core.database import SessionDep
from src.core.security import ALGORITHM, oauth2_scheme
from src.librarians.dao import librarian_dao
from src.librarians.models import Librarian
from src.librarians.schemas import TokenData


async def get_cur_librarian(
    session: SessionDep, token: str = Depends(oauth2_scheme)
) -> Librarian:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if id is None:
            raise
        token_data = TokenData(librarian_id=int(id))
    except JWTError:
        raise credentials_exception

    librarian = await librarian_dao.get_by_id(session, token_data.librarian_id)
    if not librarian:
        raise credentials_exception
    return librarian


CurLibrarianDep = Annotated[Librarian, Depends(get_cur_librarian)]
