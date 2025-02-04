from typing import Literal, TypedDict


class SearchCriteria(TypedDict):
    location: str | Literal["N/A"]
    cuisine: str | Literal["N/A"]
    budget: int | Literal["N/A"]
    rating: float | Literal["N/A"]
    guests: int | Literal["N/A"]
    time: str | Literal["N/A"]
