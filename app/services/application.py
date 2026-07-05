from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.application import application_repo
from app.schemas.app import AppInitializeResponse, RestaurantInfo, BranchInfo, AppSettings
from app.core.exceptions import NotFoundException, BadRequestException
from loguru import logger

class ApplicationService:
    async def initialize(self, db: AsyncSession, app_key: str) -> AppInitializeResponse:
        logger.info(f"Initializing app with key: {app_key}")
        
        # 1. Validate Application
        app = await application_repo.get_by_app_key(db, app_key)
        if not app:
            logger.error("Application not found")
            raise NotFoundException("Application not found or invalid app_key")
        if not app.is_enabled:
            logger.error("Application is disabled")
            raise BadRequestException("Application is currently disabled")
            
        # 2. Validate Restaurant
        restaurant = app.restaurant
        if not restaurant.is_enabled:
            logger.error(f"Restaurant {restaurant.id} is disabled")
            raise BadRequestException("Restaurant is currently disabled")

        # 3. Process Branches
        available_branches = []
        default_branch = None
        for branch in restaurant.branches:
            if branch.is_enabled:
                b_info = BranchInfo(id=branch.id, name=branch.name, is_default=branch.is_default)
                available_branches.append(b_info)
                if branch.is_default:
                    default_branch = b_info

        restaurant_info = RestaurantInfo(
            name=restaurant.name,
            logo_url=restaurant.logo_url,
            theme_color=restaurant.theme_color,
            currency=restaurant.currency,
            country=restaurant.country,
            default_branch=default_branch,
            available_branches=available_branches
        )
        
        app_settings = AppSettings(
            api_version=app.api_version
        )
        
        logger.info(f"App initialization successful for restaurant: {restaurant.name}")
        return AppInitializeResponse(restaurant=restaurant_info, settings=app_settings)

application_service = ApplicationService()
