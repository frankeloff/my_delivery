from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order

from .base import BaseCRUD


class OrdersCRUD(BaseCRUD):
    async def get_by_client_id(self, db: AsyncSession, client_id: int):
        query = select(Order).where(Order.client_id == client_id)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_order_id(self, db: AsyncSession, order_id: int):
        query = select(Order).where(Order.order_id == order_id)
        result = await db.execute(query)
        return result.scalars().first()


orders_crud = OrdersCRUD()
