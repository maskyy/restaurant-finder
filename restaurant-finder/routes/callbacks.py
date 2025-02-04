from fastapi import APIRouter, Request, Response

from ..bot.main import handle_update

router = APIRouter(prefix="/callbacks")


@router.post("/telegram")
async def telegram(request: Request):
    body = await request.json()
    await handle_update(body)
    return Response(status_code=200)
