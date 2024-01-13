from contextlib import asynccontextmanager

from fastapi import FastAPI

from public.api import users, langs
from repository import main_repo
from responses import responses


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    await main_repo.init()

    yield
    # On shutdown


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(langs.router)


@app.get("/")
def get_index():
    return responses.UNKNOWN_API_RESPONSE
