from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class BaseAPIException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(BaseAPIException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class BadRequestException(BaseAPIException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)

class UnauthorizedException(BaseAPIException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
        
    if isinstance(exc, BaseAPIException):
        logger.error(f"API Error: {exc.message} - Path: {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )
    
    if isinstance(exc, ValidationError):
        logger.error(f"Validation Error: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Validation error", "errors": exc.errors()}
        )
        
    if isinstance(exc, SQLAlchemyError):
        logger.error(f"Database Error: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error occurred"}
        )

    # Unknown errors
    logger.exception(f"Unknown Error: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"}
    )
