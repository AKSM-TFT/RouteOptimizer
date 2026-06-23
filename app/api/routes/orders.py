from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db 
from app.models.order import OrderStatus

router = APIRouter(
    prefix="/orders",    
    tags=["orders"],     
)


@router.post("/")
async def create_order(
    db: AsyncSession = Depends(get_db), 
):
    pass


@router.get("/")
async def list_orders(
    db: AsyncSession = Depends(get_db),
):
    pass


@router.get("/{order_id}")
async def get_order(
    order_id: str,  
    db: AsyncSession = Depends(get_db),
):
    pass