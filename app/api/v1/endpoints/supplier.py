from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends import get_current_user, get_session
from app.crud import supplier_crud
from app.schemas.order import OrderForStaff, ProductQuantity
from app.schemas.supplier import SupplierIn, SupplierOut

router = APIRouter()


@router.post("/", response_model=SupplierOut)
async def create_supplier(c: SupplierIn, session: AsyncSession = Depends(get_session)):
    supplier = await supplier_crud.get_by_email(session, c.email)
    if supplier is not None:
        raise HTTPException(status_code=403, detail="User already exist")
    return await supplier_crud.create(session, c)


@router.patch("/", response_model=SupplierOut)
async def update_supplier(
    email: str,
    c: SupplierIn,
    supplier=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    db_obj = await supplier_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not supplier.email == email:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await supplier_crud.update(session, db_obj, c)


@router.delete("/")
async def delete_supplier(
    email: str, supplier=Depends(get_current_user), session=Depends(get_session)
):
    db_obj = await supplier_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not supplier.email == db_obj.email:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await supplier_crud.delete(session, db_obj)


@router.get("/my_orders", response_model=List[OrderForStaff])
async def get_my_orders(
    email: str, supplier=Depends(get_current_user), session=Depends(get_session)
):
    db_obj = await supplier_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not supplier.email == db_obj.email or db_obj.position != "supplier":
        raise HTTPException(status_code=403, detail="Not enough rights")

    my_orders = await supplier_crud.get_my_orders(session, db_obj.supplier_id)
    orders = []
    for order in my_orders:
        order_list = []
        for product, quantity in zip(order.products, order.quantities):
            order_list.append(ProductQuantity(product=product, quantity=quantity))
        orders.append(OrderForStaff(order_id=order.order_id, product_list=order_list))

    return orders


@router.get("/completed_order")
async def completed_order(
    order_id: int,
    email: str,
    supplier=Depends(get_current_user),
    session=Depends(get_session),
):
    db_obj = await supplier_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not supplier.email == db_obj.email or db_obj.position != "supplier":
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await supplier_crud.completed_order(session, order_id, email)
