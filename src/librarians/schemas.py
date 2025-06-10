from pydantic import BaseModel, ConfigDict


class SLibrarian(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str


class SLibrarianCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    librarian_id: int
