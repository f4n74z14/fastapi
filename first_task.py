from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_index():
    return {"FIO": "Шепеленко Андрей Сергеевич"}


@app.get("/users")
async def get_users():
    return {"discord_id": "f4n74z14"}


@app.get("/tools")
async def get_tools():
    return {"languages": "Java, Python"}
