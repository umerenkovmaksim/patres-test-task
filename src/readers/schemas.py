from pydantic import BaseModel, EmailStr, Field


class SReader(BaseModel):
    id: int
    name: str
    email: EmailStr


class SReaderCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr


class SReaderUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    email: EmailStr | None = Field(None)
