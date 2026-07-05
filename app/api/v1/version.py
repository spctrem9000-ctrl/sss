from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/version", summary="API Version")
async def get_version():
    """
    Get the current API version.
    """
    return {
        "version": settings.API_VERSION,
        "title": settings.API_TITLE
    }
