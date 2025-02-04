from telebot import types

from .main import bot


@bot.message_handler(content_types=["text"])
async def echo(msg: types.Message):
    await bot.reply_to(msg, msg.text)
