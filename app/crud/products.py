from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Products

from .base import BaseCRUD


class ProductsCRUD(BaseCRUD):
    async def get_menu(self, db: AsyncSession, limit: int = 0, skip: int = 0):
        query = select(Products).limit(limit).offset(skip)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_price(self, db: AsyncSession, order: dict):
        result_sum = 0
        for product_id in order.keys():
            query = select(Products.price).where(Products.product_id == product_id)
            result = await db.execute(query)
            result_sum += result.scalars().first() * order[product_id]

        return result_sum


products_crud = ProductsCRUD()
