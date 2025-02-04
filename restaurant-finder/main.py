from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from .bot.handlers import *  # noqa
from .bot.main import get_bot_info, init_bot, shutdown_bot
from .config import CONFIG
from .const import PREFIX, TITLE
from .log import setup_logger
from .routes import callbacks


@asynccontextmanager
async def lifespan(_):
    setup_logger()
    await init_bot()
    await get_bot_info()
    yield
    await shutdown_bot()


app = FastAPI(
    title=TITLE,
    root_path=PREFIX,
    lifespan=lifespan,
)

root = APIRouter()
root.include_router(callbacks.router)
app.include_router(root)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=CONFIG["HOST"], port=int(CONFIG["PORT"]))
