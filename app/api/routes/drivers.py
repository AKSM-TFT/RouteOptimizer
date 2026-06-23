from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.schemas.driver import DriverCreate, DriverResponse, DriverLocationUpdate
from app.services import driver_service

router = APIRouter(
    prefix="/drivers",
    tags=["drivers"],
)


@router.post("/", response_model=DriverResponse)
async def create_driver(
    data: DriverCreate,
    db: AsyncSession = Depends(get_db),
):
    return await driver_service.create_driver(db, data)


@router.patch("/{driver_id}/location", response_model=DriverResponse)
async def update_location(
    driver_id: str,
    data: DriverLocationUpdate,
    db: AsyncSession = Depends(get_db),
):
    driver = await driver_service.update_location(db, driver_id, data)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver Not Found")
    return driver


@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(
    driver_id: str,
    db: AsyncSession = Depends(get_db),
):
    driver = await driver_service.get_driver(db, driver_id)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver Not Found")
    return driver