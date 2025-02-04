import json
import re

from openai import OpenAI

from ..config import CONFIG
from ..log import log
from ..models import NaturalQuery, tznow
from ..types import SearchCriteria

EXTRACT_PROMPT = """Extract the following details from the input and return them as a JSON object with keys:
location, cuisine, budget, rating, number_of_people, time.
If no info, use null for missing details.
For the location, translate it to English.
For the time, provide an ISO datetime string. Relate CURRENT_TIMESTAMP to the time mentioned in the input.
Return the output as JSON formatted like this:
{
  "location": "Paris",
  "cuisine": "Italian",
  "budget": 50,
  "rating": 4.4,
  "number_of_people": 3,
  "time": "CURRENT_TIMESTAMP"
}
Here is the input:
"""

ai = OpenAI(api_key=CONFIG["OPENAI_API_KEY"])


def extract_criterion(data: str, pattern: str) -> str | None:
    match = re.search(pattern, data)
    if match is None:
        return None
    group = match.group(1)
    if group == "N/A":
        return None
    return group


def extract_search_criteria(user_input: str) -> tuple[SearchCriteria, NaturalQuery]:
    natural_query, new = NaturalQuery.get_or_create(user_query=user_input)
    if not new and natural_query.parsed is not None:
        return natural_query.parsed, natural_query

    prompt = EXTRACT_PROMPT.replace("CURRENT_TIMESTAMP", tznow().strftime("%Y-%m-%dT%H:%M:%S")) + user_input
    response = ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant and a restaurant finder."},
            {"role": "user", "content": prompt},
        ],
    )

    answer = response.choices[0].message.content.strip()
    log.debug("AI answer: %s", answer)
    try:
        details = json.loads(answer)
    except json.JSONDecodeError:
        log.error("Failed to parse JSON: %s", answer)
        raise ValueError("Failed to parse OpenAI response") from None

    criteria = SearchCriteria(
        location=details.get("location", None),
        cuisine=details.get("cuisine", None),
        budget=details.get("budget", None),
        rating=details.get("rating", None),
        guests=details.get("number_of_people", None),
        time=details.get("time", None),
        latitude=None,
        longitude=None,
        answer=answer,
    )
    natural_query.parsed = criteria
    natural_query.save()

    return criteria, natural_query
