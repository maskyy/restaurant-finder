import json

from telebot.async_telebot import AsyncTeleBot, ExceptionHandler
from telebot.types import Update, User

from ..config import CONFIG
from ..const import TELEGRAM_CALLBACK_PATH
from ..log import log


class BotExceptionHandler(ExceptionHandler):
    async def handle(self, exception) -> bool:
        log.error("Bot exception", exc_info=exception)
        return False


bot = AsyncTeleBot(CONFIG["BOT_TOKEN"], exception_handler=BotExceptionHandler())


async def init_bot():
    print(CONFIG["WEBHOOK_URL"] + TELEGRAM_CALLBACK_PATH)
    await bot.set_webhook(CONFIG["WEBHOOK_URL"] + TELEGRAM_CALLBACK_PATH)


async def get_bot_info() -> User:
    user = await bot.get_me()
    log.info(user)
    return user


async def shutdown_bot():
    await bot.remove_webhook()
    await bot.close_session()


async def handle_update(body: dict[str]):
    update: Update = Update.de_json(body)

    log.debug(json.dumps(body, ensure_ascii=False))
    await bot.process_new_updates([update])
