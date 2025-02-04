from .models import Query, Restaurant
from .types import SearchCriteria


def save_query(query: SearchCriteria, restaurants: list[dict[str]]) -> Query:
    q = Query.create(
        name=query["location"],
        latitude=query["latitude"],
        longitude=query["longitude"],
    )
    for restaurant in restaurants:
        Restaurant.create(
            query=q,
            name=restaurant["name"],
            latitude=restaurant["coordinates"]["latitude"],
            longitude=restaurant["coordinates"]["longitude"],
            url=restaurant.get("url", None),
            rating=restaurant.get("rating", None),
            review_count=restaurant.get("review_count", None),
       )
    return q
