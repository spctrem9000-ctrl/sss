from typing import List, Optional
from sqlalchemy import String, Boolean, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import TimestampModel

class Category(TimestampModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False, index=True)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")


class Product(TimestampModel):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    description_ar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    is_offer: Mapped[bool] = mapped_column(Boolean, default=False)
    has_sizes: Mapped[bool] = mapped_column(Boolean, default=False)
    has_addons: Mapped[bool] = mapped_column(Boolean, default=False)
    base_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    preparation_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in minutes
    calories: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    images: Mapped[List["ProductImage"]] = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    sizes: Mapped[List["ProductSize"]] = relationship("ProductSize", back_populates="product", cascade="all, delete-orphan")
    addon_groups: Mapped[List["AddonGroup"]] = relationship("AddonGroup", secondary="product_addon_groups", back_populates="products")


class ProductImage(TimestampModel):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    product: Mapped["Product"] = relationship("Product", back_populates="images")


class ProductSize(TimestampModel):
    __tablename__ = "product_sizes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    product: Mapped["Product"] = relationship("Product", back_populates="sizes")


class AddonGroup(TimestampModel):
    __tablename__ = "addon_groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False, index=True)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    selection_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Single Choice, Multiple Choice
    minimum_required: Mapped[int] = mapped_column(Integer, default=0)
    maximum_allowed: Mapped[int] = mapped_column(Integer, default=1)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    addons: Mapped[List["Addon"]] = relationship("Addon", back_populates="group", cascade="all, delete-orphan")
    products: Mapped[List["Product"]] = relationship("Product", secondary="product_addon_groups", back_populates="addon_groups")


class Addon(TimestampModel):
    __tablename__ = "addons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    addon_group_id: Mapped[int] = mapped_column(ForeignKey("addon_groups.id"), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    group: Mapped["AddonGroup"] = relationship("AddonGroup", back_populates="addons")


class ProductAddonGroup(TimestampModel):
    __tablename__ = "product_addon_groups"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    addon_group_id: Mapped[int] = mapped_column(ForeignKey("addon_groups.id"), primary_key=True)
