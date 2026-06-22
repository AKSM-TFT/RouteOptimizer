from typing import TypedDict, Optional
from datetime import datetime


class Location(TypedDict):
    lat: float
    lng: float


class Order(TypedDict):
    id: str
    address: str
    location: Location
    priority: int          # 1 = highest
    time_window_start: Optional[datetime]
    time_window_end: Optional[datetime]
    tub_count: int


class Stop(TypedDict):
    order: Order
    sequence: int
    estimated_arrival: Optional[datetime]
    status: str            # "pending" | "completed" | "skipped"


class RouteState(TypedDict):
    driver_id: str
    driver_location: Location
    vehicle_capacity: int
    orders: list[Order]
    stops: list[Stop]
    distance_matrix: list[list[float]]
    replan_triggered: bool 
    last_planned_at: Optional[datetime]
    error: Optional[str]