from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_driver_id
from app.api.schemas.route_plan import RoutePlanCreate, RoutePlanResponse
from app.services import route_plan_service

router = APIRouter(
    prefix="/route-plans",
    tags=["route-plans"],
)


@router.post("/", response_model=RoutePlanResponse)
async def create_route_plan(
    data: RoutePlanCreate,
    driver_id: str = Depends(get_current_driver_id),
    db: AsyncSession = Depends(get_db),
):
    return await route_plan_service.create_route_plan(db, driver_id, data.order_ids)