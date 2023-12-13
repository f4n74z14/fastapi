from fastapi import FastAPI

from public.api import users
from responses import responses

app = FastAPI()
app.include_router(users.router)


@app.get("/")
def get_index():
    return responses.UNKNOWN_API_RESPONSE
