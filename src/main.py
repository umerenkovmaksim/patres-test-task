from fastapi import FastAPI

from src.core.config import settings

app = FastAPI(debug=settings.DEBUG)


@app.get("/")
async def ping():
    return "pong"
