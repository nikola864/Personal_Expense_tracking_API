from sqlalchemy.ext.asyncio import AsyncSession
from core import models
from . import schemas


async def create_category(db: AsyncSession, category: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_category(db: AsyncSession, category_id: int) -> models.Category | None:
    return await  db.get(models.Category, category_id)

