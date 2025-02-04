from urllib import parse

from aiohttp import ClientSession

from ..config import CONFIG


async def geocode_location(session: ClientSession, location: str) -> tuple[float | None, float | None]:
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = parse.urlencode("q", location, "key", CONFIG["OPENCAGE_API_KEY"])
    async with session.get(f"{url}?{params}") as response:
        data = await response.json()
        if data["results"]:
            geometry = data["results"][0]["geometry"]
            return geometry["lat"], geometry["lng"]
        return None, None
