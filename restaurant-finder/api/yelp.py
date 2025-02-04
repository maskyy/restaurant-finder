from aiohttp import ClientSession

from ..config import CONFIG
from ..models import tznow

HEADERS = {"Authorization": "Bearer " + CONFIG["YELP_API_KEY"]}


async def search_businesses(
    session: ClientSession,
    latitude: float,
    longitude: float,
    term: str | None = None,
    radius_meters: int = 1000,
    open_at: int | None = None,
    limit: int = 10,
    offset: int = 0,
) -> list[dict[str]]:
    if term is None:
        term = "restaurant"
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "term": term,
        "radius": radius_meters,
        "open_at": open_at,
        "limit": limit,
        "offset": offset,
    }
    async with session.get(url, headers=HEADERS, params=params) as response:
        data = await response.json()
        return data.get("businesses", [])
