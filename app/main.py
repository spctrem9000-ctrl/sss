from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import global_exception_handler, BaseAPIException
from app.middleware.logging import LoggingMiddleware
from app.api.router import api_router

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

def create_app() -> FastAPI:
    # Setup logging
    setup_logging()
    
    # Initialize FastAPI app
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        openapi_url="/api/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom Logging Middleware
    app.add_middleware(LoggingMiddleware)

    # Add Global Exception Handlers
    app.add_exception_handler(BaseAPIException, global_exception_handler)
    app.add_exception_handler(ValidationError, global_exception_handler)
    app.add_exception_handler(SQLAlchemyError, global_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    # Include API Routers
    app.include_router(api_router, prefix="/api")

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting up {settings.API_TITLE} - v{settings.API_VERSION}")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down API")

    return app

app = create_app()
