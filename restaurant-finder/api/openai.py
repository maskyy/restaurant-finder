import re

from openai import OpenAI

from ..config import CONFIG
from ..log import log
from ..models import NaturalQuery
from ..types import SearchCriteria

EXTRACT_PROMPT = "Extract the following details from the input: location, cuisine type, budget, rating, number of people, time. If no info, replace with N/A.\n\nInput: {user_input}\n\nDetails:"

ai = OpenAI(api_key=CONFIG["OPENAI_API_KEY"])


def extract_criterion(data: str, pattern: str) -> str | None:
    match = re.search(pattern, data)
    return match.group(1) if match else None


def extract_search_criteria(user_input: str) -> tuple[SearchCriteria, NaturalQuery]:
    natural_query, new = NaturalQuery.get_or_create(query=user_input)
    if not new and natural_query.parsed is not None:
        return natural_query.parsed, natural_query

    response = ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant and a restaurant finder."},
            {"role": "user", "content": EXTRACT_PROMPT.format(user_input=user_input)},
        ],
    )

    answer = response.choices[0].message.content.strip()
    log.debug("AI answer: %s", answer)
    details = answer.split("\n")

    criteria = SearchCriteria(
        location=extract_criterion(details[0], r"Location: (.+)"),
        cuisine=extract_criterion(details[1], r"Cuisine type: (.+)"),
        budget=extract_criterion(details[2], r"Budget: (\d+)"),
        rating=extract_criterion(details[3], r"Rating: (\d+\.\d+)"),
        guests=extract_criterion(details[4], r"Number of people: (\d+)"),
        time=extract_criterion(details[5], r"Time: (.+)"),
        latitude=None,
        longitude=None,
        answer=answer,
    )
    if criteria["budget"] is not None:
        criteria["budget"] = int(criteria["budget"])
    if criteria["rating"] is not None:
        criteria["rating"] = float(criteria["rating"])
    if criteria["guests"] is not None:
        criteria["guests"] = int(criteria["guests"])
    natural_query.parsed = criteria
    natural_query.save()

    return criteria, natural_query
