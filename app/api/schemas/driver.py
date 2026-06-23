from pydantic import BaseModel, Field
from typing import Optional
from app.api.schemas.order import LocationSchema


class DriverCreate(BaseModel):
    name: str
    vehicle_capacity: int = Field(..., ge=1)


class DriverLocationUpdate(BaseModel):
    location: LocationSchema  


class DriverResponse(BaseModel):
    id: str
    name: str
    vehicle_capacity: int
    current_lat: Optional[float]
    current_lng: Optional[float]

    model_config = {"from_attributes": True}