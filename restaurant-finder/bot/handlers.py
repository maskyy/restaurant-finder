from datetime import datetime

from aiohttp import ClientSession
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..api.openai import extract_search_criteria
from ..api.opencage import geocode_location
from ..api.yelp import search_businesses
from ..config import CONFIG
from ..database import save_query
from ..log import log
from ..models import Query
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


def prepare_answer(query: Query) -> tuple[str, list[InlineKeyboardMarkup]]:
    if len(query.restaurants) == 0:
        return f"No restaurants found at '{query.name}' :(", []

    text = f"I've found the following places at '{query.name}':"
    for restaurant in query.restaurants:
        name = restaurant.name
        if restaurant.url is not None:
            name = f"[{name}]({restaurant.url})"
        in_braces = []
        if restaurant.price is not None:
            in_braces.append(restaurant.price)
        if restaurant.rating is not None:
            in_braces.append(f"{restaurant.rating} stars")
        if restaurant.review_count is not None:
            in_braces.append(f"{restaurant.review_count} reviews")
        text += f"\n- {name} ({', '.join(in_braces)})"

    button = InlineKeyboardButton(
        text="Show on map",
        url=CONFIG["SERVER_URL"] + "/query/" + str(query.id),
    )
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(button)
    return text, markup


@bot.message_handler(content_types=["text"])
async def find_restaurants(msg: types.Message):
    try:
        criteria, nq = extract_search_criteria(msg.text)
    except ValueError:
        return await bot.reply_to(msg, "Sorry, I couldn't understand the query.")

    if criteria["location"] is None:
        return await bot.reply_to(msg, "Sorry, I couldn't understand the location.")
    async with ClientSession() as session:
        if criteria["latitude"] is None:
            lat, lon = await geocode_location(session, criteria["location"])
            criteria["latitude"] = lat
            criteria["longitude"] = lon
        if criteria["latitude"] is None:
            return await bot.reply_to(msg, "Sorry, I couldn't understand the location " + criteria["location"])

        nq.parsed = criteria
        nq.save()
        query = nq.query
        if query is None:
            terms = criteria["cuisine"]
            open_at = None
            if criteria["time"] is not None:
                open_at = int(datetime.fromisoformat(criteria["time"]).timestamp())

            restaurants = await search_businesses(
                session,
                criteria["latitude"],
                criteria["longitude"],
                terms,
                open_at=open_at,
            )
            query = save_query(criteria, restaurants)
            nq.query = query
            nq.save()

    log.debug("Query %s: %d restaurants", str(query.id), len(query.restaurants))
    text, buttons = prepare_answer(query)
    await bot.reply_to(msg, text, reply_markup=buttons, parse_mode="Markdown")


@bot.message_handler(content_types=["location"])
async def handle_location(msg: types.Message):
    await bot.reply_to(msg, "Received location (stub)")


@bot.message_handler(func=lambda _: True)
async def unknown_message(msg: types.Message):
    await bot.reply_to(msg, "Sorry, I don't understand that command.")
