from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from core import models
from . import schemas

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db:AsyncSession, user_id: int) -> models.User | None:
    return await db.get(models.User, user_id)

