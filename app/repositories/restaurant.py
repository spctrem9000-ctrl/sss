from app.repositories.base import BaseRepository
from app.models.restaurant import Restaurant
from pydantic import BaseModel

class RestaurantRepository(BaseRepository[Restaurant, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Restaurant)

restaurant_repo = RestaurantRepository()
