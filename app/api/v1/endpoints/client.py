from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends import get_current_user, get_session
from app.crud import client_crud, products_crud
from app.schemas.client import ClientIn, ClientOut
from app.schemas.order import GetOrder, Order
from app.schemas.products import ProductsOut

router = APIRouter()


@router.post("/", response_model=ClientOut)
async def create_client(c: ClientIn, session: AsyncSession = Depends(get_session)):
    client = await client_crud.get_by_email(session, c.email)
    if client is not None:
        raise HTTPException(status_code=403, detail="User already exist")
    return await client_crud.create(session, c)


@router.patch("/", response_model=ClientOut)
async def update_client(
    email: str,
    c: ClientIn,
    client=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    db_obj = await client_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not client.email == email:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await client_crud.update(session, db_obj, c)


@router.delete("/")
async def delete_client(
    email: str, client=Depends(get_current_user), session=Depends(get_session)
):
    db_obj = await client_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not client.email == db_obj.email:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await client_crud.delete(session, db_obj)


@router.get("/", response_model=List[ProductsOut])
async def get_menu(
    limit: int = 100,
    skip: int = 0,
    client=Depends(get_current_user),
    session=Depends(get_session),
):
    return await products_crud.get_menu(session, limit, skip)


@router.post("/make_an_order", response_model=Order)
async def make_an_order(
    order: List[int],
    email: str,
    client=Depends(get_current_user),
    session=Depends(get_session),
):
    db_obj = await client_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not client.email == db_obj.email:
        raise HTTPException(status_code=403, detail="Not enough rights")
    res_dict = await client_crud.make_an_order(session, db_obj.client_id, order)
    return Order(**res_dict)


@router.get("/my_order", response_model=GetOrder)
async def get_my_order(
    email: str,
    client=Depends(get_current_user),
    session=Depends(get_session),
):
    db_obj = await client_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not client.email == db_obj.email:
        raise HTTPException(status_code=403, detail="Not enough rights")
    my_orders = await client_crud.get_my_orders(session, db_obj.client_id)
    return my_orders


@router.delete("/accept_the_order", response_model=bool)
async def accept_the_order(
    order_id: int,
    email: str,
    client=Depends(get_current_user),
    session=Depends(get_session),
):
    db_obj = await client_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not client.email == db_obj.email:
        raise HTTPException(status_code=403, detail="Not enough rights")

    answer = await client_crud.accept_order(session, order_id)

    if not answer:
        raise HTTPException(status_code=404, detail="Order not found")

    return answer
