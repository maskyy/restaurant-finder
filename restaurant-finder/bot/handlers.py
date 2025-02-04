from telebot import types

from ..ai.main import extract_details
from .main import bot


@bot.message_handler(content_types=["text"])
async def echo(msg: types.Message):
    details = extract_details(msg.text)
    await bot.reply_to(msg, details)
