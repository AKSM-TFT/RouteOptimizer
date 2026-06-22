from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(String(36), primary_key=True)
    name = Column(String, nullable=False)
    vehicle_capacity = Column(Integer, nullable=False)   
    current_lat = Column(Float, nullable=True)       
    current_lng = Column(Float, nullable=True)

    route_plans = relationship("RoutePlan", back_populates="driver")