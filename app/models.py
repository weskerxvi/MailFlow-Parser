from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime
from datetime import datetime, timezone

from app.database import Base
 
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(Integer)
    client: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= lambda: datetime.now(timezone.utc)
    )
    