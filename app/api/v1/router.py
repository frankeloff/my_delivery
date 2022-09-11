from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends import get_session
from app.api.v1.endpoints.chef import router as chef_router
from app.api.v1.endpoints.client import router as client_router
from app.api.v1.endpoints.supplier import router as supplier_router
from app.core.const import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import create_access_token
from app.crud import user_crud
from app.models.token import Token

api_router = APIRouter()


@api_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    db_obj = await user_crud.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_obj.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


api_router.include_router(client_router, prefix="/client")
api_router.include_router(chef_router, prefix="/chef")
api_router.include_router(supplier_router, prefix="/supplier")
