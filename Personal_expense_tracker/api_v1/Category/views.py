from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from . import schemas, crud

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.CategoryResponse, status_code=201)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(db, category)

@router.get("/{category_id}", response_model=schemas.CategoryResponse)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    db_category = await crud.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

