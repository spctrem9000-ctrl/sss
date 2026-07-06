from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import global_exception_handler, BaseAPIException
from app.middleware.logging import LoggingMiddleware
from app.api.router import api_router

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


async def run_migrations():
    """Run database migrations using SQLAlchemy create_all (safe for production)."""
    try:
        from app.database.session import engine
        from app.models.base import Base
        # Import all models to register them with Base
        import app.models.admin
        import app.models.application
        import app.models.branch
        import app.models.cart
        import app.models.checkout
        import app.models.customer
        import app.models.hub
        import app.models.menu
        import app.models.order
        import app.models.otp
        import app.models.restaurant
        import app.models.token

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info(f"Starting up {settings.API_TITLE} - v{settings.API_VERSION}")
    await run_migrations()
    yield
    logger.info("Shutting down API")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        openapi_url="/api/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(LoggingMiddleware)

    app.add_exception_handler(StarletteHTTPException, global_exception_handler)
    app.add_exception_handler(RequestValidationError, global_exception_handler)
    app.add_exception_handler(BaseAPIException, global_exception_handler)
    app.add_exception_handler(ValidationError, global_exception_handler)
    app.add_exception_handler(SQLAlchemyError, global_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
