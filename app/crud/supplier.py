import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models import Order, OrderDetails, Products, Supplier
from app.schemas.supplier import SupplierIn

from .base import BaseCRUD
from .orders import orders_crud


class SupplierCRUD(BaseCRUD):
    async def create(self, db: AsyncSession, c: SupplierIn):
        password = c.password
        c.password = get_password_hash(password)
        db_obj = Supplier(**c.dict())

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(self, db: AsyncSession, db_obj: Supplier, update_obj: SupplierIn):
        encoded_object_in = jsonable_encoder(db_obj)
        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict()

        update_data["updated_at"] = datetime.datetime.now()

        for field in encoded_object_in:
            if field in update_data:
                if field == "password":
                    setattr(db_obj, field, get_password_hash(update_data[field]))
                else:
                    setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def delete(self, db: AsyncSession, db_obj: Supplier):

        await db.delete(db_obj)
        await db.commit()

        return True

    async def get_by_id(self, db: AsyncSession, id: int):
        query = select(Supplier).where(Supplier.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str):
        query = select(Supplier).where(Supplier.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def authenticate_client(self, db: AsyncSession, id: int, password: str):
        db_obj = await self.get_by_id(db, id)
        if not verify_password(password, db_obj.password):
            return False
        return db_obj

    async def get_my_orders(self, db: AsyncSession, supplier_id: int):
        query = (
            select(
                Order.order_id,
                func.array_agg(Products.name).label("products"),
                func.array_agg(OrderDetails.quantity).label("quantities"),
            )
            .select_from(Supplier)
            .join(Order, Supplier.supplier_id == Order.supplier_id, isouter=True)
            .join(OrderDetails, Order.order_id == OrderDetails.order_id, isouter=True)
            .join(
                Products, OrderDetails.product_id == Products.product_id, isouter=True
            )
            .where(
                and_(Supplier.supplier_id == supplier_id, Order.status == "supplier")
            )
            .group_by(Order.order_id)
        )

        result = await db.execute(query)

        return result.fetchall()

    async def completed_order(self, db: AsyncSession, order_id: int, email: str):
        db_obj = await orders_crud.get_by_order_id(db, order_id)
        setattr(db_obj, "status", "delivered")
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        supplier = await supplier_crud.get_by_email(db, email)
        supplier.number_of_orders -= 1
        db.add(supplier)
        await db.commit()

        return 0


supplier_crud = SupplierCRUD()
