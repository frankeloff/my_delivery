from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Products

from .base import BaseCRUD


class ProductsCRUD(BaseCRUD):
    async def get_menu(self, db: AsyncSession, limit: int = 0, skip: int = 0):
        query = select(Products).limit(limit).offset(skip)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_price(self, db: AsyncSession, order: list):
        query = select(func.sum(Products.price)).filter(Products.product_id.in_(order))
        result_sum = await db.execute(query)
        return result_sum.scalars().first()


products_crud = ProductsCRUD()
