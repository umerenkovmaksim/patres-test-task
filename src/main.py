from fastapi import FastAPI

from src.books.router import router as books_router
from src.core.config import settings
from src.librarians.router import router as librarians_router

app = FastAPI(debug=settings.DEBUG)


@app.get("/", tags=["Root"])
async def ping():
    return "pong"


app.include_router(librarians_router)
app.include_router(books_router)
