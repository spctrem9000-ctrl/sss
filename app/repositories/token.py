from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.token import RefreshToken
from pydantic import BaseModel

class TokenCreate(BaseModel):
    customer_id: int
    token_hash: str
    expires_at: datetime

class TokenRepository(BaseRepository[RefreshToken, TokenCreate, BaseModel]):
    def __init__(self):
        super().__init__(RefreshToken)

token_repo = TokenRepository()
