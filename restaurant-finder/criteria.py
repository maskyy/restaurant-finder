from typing import TypedDict


class SearchCriteria(TypedDict):
    location: str | None
    cuisine: str | None
    budget: int | None
    rating: float | None
    guests: int | None
    time: str | None
    radius: int
    intro_text: str
    latitude: float | None
    longitude: float | None
    answer: str
