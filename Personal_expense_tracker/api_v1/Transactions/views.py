from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from . import schemas, crud
from api_v1.User.crud import get_user
from api_v1.Category.crud import get_category


router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=schemas.TransactionResponse, status_code=201)
async def create_transaction(transaction: schemas.TransactionCreate, db: AsyncSession = Depends(get_db)):
    if not await get_user(db, transaction.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not await get_category(db, transaction.category_id):
        raise HTTPException(status_code=404, detail="Category not found")

    return await crud.create_transaction(db, transaction)

@router.get("/", response_model=list[schemas.TransactionResponse])
async def read_transactions(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        user_id: int | None = None,
        category_id: int | None = None,
        type: str | None = Query(None, pattern="^(income|expense)$"),
        db: AsyncSession = Depends(get_db),
):
    is_income = {"income": True, "expense": False}.get(type) if type else None
    return await crud.get_transactions(db, skip, limit, user_id, category_id, is_income)

@router.get("/paginated/")
async def paginated_transactions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    user_id: int | None = None,
    type: str | None = Query(None, pattern="^(income|expense)$"),
    db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * size
    is_income = {"income": True, "expense": False}.get(type)
    transactions = await crud.get_transactions(db, skip, size, user_id=user_id, is_income=is_income)
    total = len(transactions)
    return {
        "items": transactions,
        "page": page,
        "size": size,
        "total": total,
        "pages": (total + size - 1) // size
    }

@router.get("balance/{user_id}")
async def get_user_balance(user_id: int, db: AsyncSession = Depends(get_db)):
    if not await get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.get_balance(db, user_id)

@router.get("/export/json/{user_id}")
async def export_user_transactions(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = await crud.get_transactions(db, user_id=user_id)
    data = [
        {
            "id": t.id,
            "amount": float(t.amount),
            "description": t.description,
            "date": t.date.isoformat(),
            "category": t.category.name,
            "type": "income" if t.category.is_income else "expense"
        }
        for t in transactions
    ]
    return {"user_id": user_id, "transactions": data}
















