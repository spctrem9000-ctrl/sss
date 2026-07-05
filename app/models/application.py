from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import TimestampModel

class Application(TimestampModel):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    app_key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    api_version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="applications")
