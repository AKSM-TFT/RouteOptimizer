from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order, OrderStatus
from app.api.schemas.order import OrderCreate
import uuid


async def create_order(db: AsyncSession, data: OrderCreate) -> Order:
    order = Order(
        id=str(uuid.uuid4()), 
        address=data.address,
        lat=data.location.lat,
        lng=data.location.lng,
        priority=data.priority,
        time_window_start=data.time_window_start,
        time_window_end=data.time_window_end,
        tub_count=data.tub_count,
        status=OrderStatus.pending,  
    )
    db.add(order) 
    await db.commit() 
    await db.refresh(order)  

    return order


async def get_order(db: AsyncSession, order_id: str) -> Order | None:
    result = await db.execute(
        select(Order).where(Order.id == order_id)  
    )
    return result.scalars().first()


async def list_orders(db: AsyncSession) -> list[Order]:
    result = await db.execute(select(Order))
    return result.scalars().all()