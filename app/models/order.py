from sqlalchemy import Column, String, Integer, Float, DateTime, Enum
from app.models.base import Base
import enum

class OrderStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    skipped = "skipped"

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True)
    address = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    priority = Column(Integer, default=3)
    time_window_start = Column(DateTime, nullable=True)
    time_window_end = Column(DateTime, nullable=True)
    tub_count = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)