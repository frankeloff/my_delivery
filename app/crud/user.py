from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models.user import User

from .base import BaseCRUD


class UserCRUD(BaseCRUD):
    async def get_by_id(self, db: AsyncSession, id: int):
        query = select(User).where(User.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str):
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def authenticate_user(self, db: AsyncSession, email: str, password: str):
        db_obj = await self.get_by_email(db, email)
        if not verify_password(password, db_obj.password):
            return False
        return db_obj


user_crud = UserCRUD()
