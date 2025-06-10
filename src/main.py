from fastapi import FastAPI

from src.core.config import settings
from src.librarians.router import router as librarian_router

app = FastAPI(debug=settings.DEBUG)


@app.get("/")
async def ping():
    return "pong"


app.include_router(librarian_router)
