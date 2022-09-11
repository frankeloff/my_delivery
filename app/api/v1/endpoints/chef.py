from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends import get_current_user, get_session
from app.crud import chef_crud
from app.schemas.chef import ChefIn, ChefOut
from app.schemas.order import OrderForStaff

router = APIRouter()


@router.post("/", response_model=ChefOut)
async def create_chef(c: ChefIn, session: AsyncSession = Depends(get_session)):
    chef = await chef_crud.get_by_email(session, c.email)
    if chef is not None:
        raise HTTPException(status_code=403, detail="User already exist")
    return await chef_crud.create(session, c)


@router.patch("/", response_model=ChefOut)
async def update_chef(
    email: str,
    c: ChefIn,
    chef=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    db_obj = await chef_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not chef.email == email:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await chef_crud.update(session, db_obj, c)


@router.delete("/")
async def delete_chef(
    email: str, chef=Depends(get_current_user), session=Depends(get_session)
):
    db_obj = await chef_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not chef.email == db_obj.email:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await chef_crud.delete(session, db_obj)


@router.get("/my_orders", response_model=List[OrderForStaff])
async def get_my_orders(
    email: str, chef=Depends(get_current_user), session=Depends(get_session)
):
    db_obj = await chef_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not chef.email == db_obj.email:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await chef_crud.get_my_orders(session, db_obj.chef_id)


@router.get("/completed_order")
async def completed_order(
    order_id: int,
    email: str,
    chef=Depends(get_current_user),
    session=Depends(get_session),
):
    db_obj = await chef_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if not chef.email == db_obj.email or db_obj.position != "chef":
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await chef_crud.completed_order(session, order_id, email)
