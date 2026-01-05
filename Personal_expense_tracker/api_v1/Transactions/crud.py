from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from core import models
from . import schemas

async def create_transaction(db: AsyncSession, transaction: schemas.TransactionCreate) -> models.Transaction:
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_transactions(
        db: AsyncSession,
        skip: int=0,
        limit: int=10,
        user_id: int | None = None,
        category_id: int | None = None,
        is_income: bool | None = None,
):
    stmt = select(models.Transaction)

    if user_id is not None:
        stmt = stmt.where(models.Transaction.user_id == user_id)
    if category_id is not None:
        stmt = stmt.where(models.Transaction.category_id == category_id)
    if is_income is not None:
        stmt = stmt.join(models.Category).where(models.Category.is_income == is_income)

    stmt = stmt.offset(skip).limit(limit).order_by(models.Transaction.date.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_balance(db: AsyncSession, user_id: int) -> dict:
    income_stmt = (
        select(func.coalesce(func.sum(models.Transaction.amount), 0.0)).join(models.Category).where(
            models.Transaction.user_id == user_id,
            models.Category.is_income == True,
        )
    )

    expense_stmt = (
        select(func.coalesce(func.sum(models.Transaction.amount), 0.0))
        .join(models.Category)
        .where(
            models.Transaction.user_id == user_id,
            models.Category.is_income == False
        )
    )

    income = (await db.execute(income_stmt)).scalar()
    expense = (await db.execute(expense_stmt)).scalar()
    return {"income": float(income), "expense": float(expense), "balance": float(income - expense)}







