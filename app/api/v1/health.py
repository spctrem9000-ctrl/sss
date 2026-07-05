from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database.session import get_db_session

router = APIRouter()

@router.get("/health", summary="Health Check")
async def health_check(db: AsyncSession = Depends(get_db_session)):
    """
    Health check endpoint.
    """
    db_status = "connected"
    try:
        # Check database connection
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    return {
        "status": "ok",
        "database": db_status,
        "version": "1.0.0"
    }
