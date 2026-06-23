from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db 
from app.models.order import OrderStatus
from app.api.schemas.order import OrderCreate, OrderResponse
from app.services import order_service


router = APIRouter(
    prefix="/orders",    
    tags=["orders"],     
)


@router.post("/", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,  
    db: AsyncSession = Depends(get_db),
):
    order = await order_service.create_order(db, data)
    return order


@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    db: AsyncSession = Depends(get_db),
):
    return await order_service.list_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    db: AsyncSession = Depends(get_db),
):
    order = await order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order