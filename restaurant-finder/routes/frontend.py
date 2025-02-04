from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ..config import CONFIG

BASE_PATH = Path(CONFIG["DIST_DIR"]).resolve()
INDEX_PATH = BASE_PATH / "index.html"

router = APIRouter(prefix="")


@router.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Ensure no path traversal
    try:
        path = BASE_PATH.joinpath(BASE_PATH.joinpath(full_path).resolve().relative_to(BASE_PATH))
    except ValueError:
        raise HTTPException(status_code=403, detail="Forbidden") from None

    if path.exists() and path.is_file():
        return FileResponse(path)
    return FileResponse(INDEX_PATH)
