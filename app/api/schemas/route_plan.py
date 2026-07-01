from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class StopItem(BaseModel):
    order_id: str
    sequence: int      
    lat: float
    lng: float
    eta: Optional[datetime] = None

class RoutePlanStatus(str, Enum):
    pending = "pending"
    active = "active"
    completed = "completed"
    superseded = "superseded"  

class RoutePlanCreate(BaseModel):
    order_ids: list[str]

class RoutePlanResponse(BaseModel):
    id: str
    driver_id: str
    status: RoutePlanStatus
    stop_sequence: list[StopItem]
    created_at: Optional[datetime]
    last_updated: Optional[datetime]

    class Config:
        from_attributes = True