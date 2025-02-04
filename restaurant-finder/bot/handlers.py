from telebot import types

from ..ai.main import extract_search_criteria
from .main import bot

START_TEXT = """
Welcome to RestFind! What restaurants are you looking for? You can include the following:
- Location: where? (required)
- Cuisine type: what?
- Budget: how much?
- Rating: how well rated?
- Number of people: how many guests?
- Time: when?
"""


@bot.message_handler(commands=["start"])
async def start_command(msg: types.Message):
    await bot.reply_to(msg, START_TEXT)


@bot.message_handler(content_types=["text"])
async def find_restaurants(msg: types.Message):
    criteria = extract_search_criteria(msg.text)
    if criteria["location"] is None:
        return await bot.reply_to(msg, "Sorry, I couldn't understand the location.")

    await bot.reply_to(msg, criteria)


@bot.message_handler(content_types=["location"])
async def handle_location(msg: types.Message):
    await bot.reply_to(msg, "Received location (stub)")


@bot.message_handler(func=lambda _: True)
async def unknown_message(msg: types.Message):
    await bot.reply_to(msg, "Sorry, I don't understand that command.")

