from fastapi import FastAPI
import uvicorn

from db.database import init_db, close_db

async def lifespan(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        await close_db()

app = FastAPI(lifespan=lifespan)

def main() -> FastAPI:


    return app

appMain = main()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)