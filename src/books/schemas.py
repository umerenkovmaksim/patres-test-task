from pydantic import BaseModel, ConfigDict, Field


class SBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    author: str
    year: int | None
    isbn: str | None
    copies: int


class SBookCreate(BaseModel):
    name: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: int | None = Field(None)
    isbn: str | None = Field(None)
    copies: int = Field(1, ge=0)


class SBookUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    author: str | None = Field(None, min_length=1)
    year: int | None = Field(None)
    isbn: str | None = Field(None)
    copies: int | None = Field(None, ge=0)
