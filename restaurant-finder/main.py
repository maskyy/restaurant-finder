from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .bot.handlers import *  # noqa
from .bot.main import get_bot_info, init_bot, shutdown_bot
from .config import CONFIG
from .const import PREFIX, TITLE
from .log import setup_logger
from .models import create_tables
from .routes import callbacks, frontend, queries


@asynccontextmanager
async def lifespan(_):
    setup_logger()
    create_tables()
    await init_bot()
    await get_bot_info()
    yield
    await shutdown_bot()


app = FastAPI(
    title=TITLE,
    openapi_docs=PREFIX + "/openapi.json",
    docs_url=PREFIX + "/docs",
    redoc_url=PREFIX + "/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CONFIG["SERVER_URL"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix=PREFIX)
api.include_router(callbacks.router)
api.include_router(queries.router)
app.include_router(api)
app.include_router(frontend.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=CONFIG["HOST"], port=int(CONFIG["PORT"]))
