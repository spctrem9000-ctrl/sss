from app.repositories.base import BaseRepository
from app.models.branch import Branch
from pydantic import BaseModel

class BranchRepository(BaseRepository[Branch, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Branch)

branch_repo = BranchRepository()
