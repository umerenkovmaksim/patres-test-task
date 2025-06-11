from pydantic import BaseModel, ConfigDict, EmailStr


class SLibrarian(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class SLibrarianCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    librarian_id: int
