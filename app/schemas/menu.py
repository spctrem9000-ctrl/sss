from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, ConfigDict
from datetime import datetime

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

class CategoryResponse(BaseModel):
    id: int
    name_ar: str
    name_en: str
    image: Optional[str] = None
    sort_order: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    sort_order: int

    model_config = ConfigDict(from_attributes=True)

class ProductSizeResponse(BaseModel):
    id: int
    name_ar: str
    name_en: str
    price: float
    sort_order: int

    model_config = ConfigDict(from_attributes=True)

class AddonResponse(BaseModel):
    id: int
    name_ar: str
    name_en: str
    price: float
    is_available: bool
    sort_order: int

    model_config = ConfigDict(from_attributes=True)

class AddonGroupResponse(BaseModel):
    id: int
    name_ar: str
    name_en: str
    selection_type: str
    minimum_required: int
    maximum_allowed: int
    sort_order: int
    addons: List[AddonResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ProductResponse(BaseModel):
    id: int
    category_id: int
    name_ar: str
    name_en: str
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    image: Optional[str] = None
    is_available: bool
    is_featured: bool = False
    is_hidden: bool = False
    is_offer: bool = False
    has_sizes: bool
    has_addons: bool
    base_price: float
    preparation_time: Optional[int] = None
    calories: Optional[int] = None
    sort_order: int
    
    images: List[ProductImageResponse] = []
    sizes: List[ProductSizeResponse] = []
    addon_groups: List[AddonGroupResponse] = []

    model_config = ConfigDict(from_attributes=True)

class MenuResponse(BaseModel):
    categories: List[CategoryResponse]
    products: List[ProductResponse]
    
    model_config = ConfigDict(from_attributes=True)
