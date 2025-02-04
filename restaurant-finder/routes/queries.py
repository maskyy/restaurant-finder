from fastapi import APIRouter, HTTPException

from ..models import Query

router = APIRouter(prefix="/queries")


@router.get("/{id}")
async def get_query(id: str):
    query = Query.get_or_none(Query.id == id)
    if query is None:
        raise HTTPException(status_code=404, detail="Query not found")

    data = {
        "current_location": {
            "latitude": query.latitude,
            "longitude": query.longitude,
        },
        "restaurants": [
            {
                "name": restaurant.name,
                "price": restaurant.price,
                "latitude": restaurant.latitude,
                "longitude": restaurant.longitude,
                "url": restaurant.url,
                "rating": restaurant.rating,
                "review_count": restaurant.review_count,
            }
            for restaurant in query.restaurants
        ],
    }

    return data
