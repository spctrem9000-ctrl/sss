from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas.app import AppInitializeRequest, AppInitializeResponse
from app.services.application import application_service

router = APIRouter()

@router.post(
    "/initialize",
    response_model=AppInitializeResponse,
    status_code=status.HTTP_200_OK,
    summary="Initialize Application",
    description="Validates the app key and returns the restaurant information, branches, and app settings.",
    responses={
        200: {"description": "Successful Initialization"},
        400: {"description": "Application or Restaurant Disabled"},
        404: {"description": "Application not found"}
    }
)
async def initialize_app(
    request: AppInitializeRequest,
    db: AsyncSession = Depends(get_db_session)
):
    return await application_service.initialize(db, request.app_key)
