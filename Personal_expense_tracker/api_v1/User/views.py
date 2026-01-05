from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from . import schemas, crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse, status_code=201)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db, user)
    return db_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


