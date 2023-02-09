import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models import Chef, Client, Order, OrderDetails, Products, Supplier
from app.schemas.client import ClientIn

from .base import BaseCRUD
from .chef import chef_crud
from .orders import orders_crud
from .products import products_crud
from .supplier import supplier_crud


class ClientCRUD(BaseCRUD):
    async def create(self, db: AsyncSession, c: ClientIn):
        password = c.password
        c.password = get_password_hash(password)
        db_obj = Client(**c.dict())

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(self, db: AsyncSession, db_obj: Client, update_obj: ClientIn):
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

    async def delete(self, db: AsyncSession, db_obj: Client):
        await db.delete(db_obj)
        await db.commit()

        return True

    async def get_by_email(self, db: AsyncSession, email: str):
        query = select(Client).where(Client.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_id(self, db: AsyncSession, id: int):
        query = select(Client).where(Client.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def authenticate_client(self, db: AsyncSession, email: str, password: str):
        db_obj = await self.get_by_email(db, email)
        if not verify_password(password, db_obj.password):
            return False
        return db_obj

    async def get_free_chef(self, db: AsyncSession):
        query = select(Chef).order_by(Chef.number_of_orders)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_free_supplier(self, db: AsyncSession):
        query = select(Supplier).order_by(Supplier.number_of_orders)
        result = await db.execute(query)
        return result.scalars().first()

    async def make_an_order(self, db: AsyncSession, client_id: int, product_dict: dict):
        chef = await self.get_free_chef(db)
        supplier = await self.get_free_supplier(db)
        price = await products_crud.get_price(db, product_dict)

        db_order_obj = Order(
            chef_id=chef.chef_id,
            supplier_id=supplier.supplier_id,
            client_id=client_id,
            price=price,
            status="chef",
        )
        db.add(db_order_obj)
        await db.commit()
        await db.refresh(db_order_obj)

        order_details_list = []
        for product in product_dict.keys():
            db_order_details_obj = OrderDetails(
                order_id=db_order_obj.order_id,
                product_id=product,
                quantity=product_dict[product],
            )
            order_details_list.append(db_order_details_obj)

        db.add_all(order_details_list)
        await db.commit()

        chef.number_of_orders += 1
        db.add(chef)
        await db.commit()

        supplier.number_of_orders += 1
        db.add(supplier)
        await db.commit()

        return {
            "chef_name": chef.first_name,
            "supplier_name": supplier.first_name,
            "price": price,
        }

    async def get_my_orders(self, db: AsyncSession, client_id: int):
        query = (
            select(
                Order.order_id,
                func.array_agg(Products.name).label("products"),
                func.array_agg(OrderDetails.quantity).label("quantities"),
                Order.price,
            )
            .select_from(Client)
            .join(Order, Client.client_id == Order.client_id, isouter=True)
            .join(OrderDetails, Order.order_id == OrderDetails.order_id, isouter=True)
            .join(
                Products, OrderDetails.product_id == Products.product_id, isouter=True
            )
            .where(Client.client_id == client_id)
            .group_by(Order.order_id)
        )

        result = await db.execute(query)
        return result.fetchall()

    async def accept_order(self, db: AsyncSession, order_id: int):
        query = select(Order).where(Order.order_id == order_id)
        result = await db.execute(query)
        my_order = result.scalars().first()
        if not my_order.status == "delivered":
            return False
        query = delete(OrderDetails).where(OrderDetails.order_id == order_id)
        await db.execute(query)

        await db.delete(my_order)
        await db.commit()

        return True


client_crud = ClientCRUD()
