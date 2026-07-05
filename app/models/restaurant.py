from typing import List
from sqlalchemy import String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import TimestampModel

class Restaurant(TimestampModel):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    theme_color: Mapped[str] = mapped_column(String(50), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="USA")
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    settings: Mapped[dict] = mapped_column(JSON, nullable=True)

    branches: Mapped[List["Branch"]] = relationship("Branch", back_populates="restaurant")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="restaurant")
