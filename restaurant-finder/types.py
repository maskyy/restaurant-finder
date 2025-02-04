from typing import Literal, TypedDict


class SearchCriteria(TypedDict):
    location: str | None
    cuisine: str | None
    budget: int | None
    rating: float | None
    guests: int | None
    time: str | None
    latitude: float | None
    longitude: float | None
    answer: str
