from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.driver import Driver
from app.api.schemas.driver import DriverCreate, DriverLocationUpdate
import uuid


async def create_driver(db: AsyncSession, data: DriverCreate) -> Driver:
    driver = Driver(
        id=str(uuid.uuid4()),
        name=data.name,
        vehicle_capacity=data.vehicle_capacity,
    )
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    return driver


async def update_location(db: AsyncSession, driver_id: str, data: DriverLocationUpdate) -> Driver | None:
    driver = await db.get(Driver, driver_id)  
    if driver is None:
        return None
    driver.current_lat = data.location.lat
    driver.current_lng = data.location.lng
    await db.commit()
    await db.refresh(driver)
    return driver


async def get_driver(db: AsyncSession, driver_id: str) -> Driver | None:
    return await db.get(Driver, driver_id) 