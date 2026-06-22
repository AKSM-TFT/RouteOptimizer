from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class RoutePlan(Base):
    __tablename__ = "route_plans"

    id = Column(String(36), primary_key=True)
    driver_id = Column(String(36), ForeignKey("drivers.id"), nullable=False) 
    stop_sequence = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False)
    last_updated = Column(DateTime, nullable=False)

    driver = relationship("Driver", back_populates="route_plans")