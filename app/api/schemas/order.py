from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime
from app.models.order import OrderStatus

class LocationSchema(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

class OrderCreate(BaseModel):
    address: str
    location: LocationSchema
    priority: int = Field(default=3, ge=1, le=5)
    time_window_start: Optional[datetime] = None
    time_window_end: Optional[datetime] = None
    tub_count: int = Field(..., ge=1)

class OrderResponse(BaseModel):
    id: str
    address: str
    location: LocationSchema
    priority: int
    time_window_start: Optional[datetime]
    time_window_end: Optional[datetime]
    tub_count: int
    status: OrderStatus

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def build_location(cls, values):
        lat = getattr(values, "lat", None) or (values.get("lat") if isinstance(values, dict) else None)
        lng = getattr(values, "lng", None) or (values.get("lng") if isinstance(values, dict) else None)
        if lat is not None and lng is not None:
            if isinstance(values, dict):
                values["location"] = {"lat": lat, "lng": lng}
            else:
                values.location = LocationSchema(lat=lat, lng=lng)
        return values