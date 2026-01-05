from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import engine
from core import models
from api_v1.User.views import router as user_router
from api_v1.Category.views import router as category_router
from api_v1.Transactions.views import router as transaction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    print("✅ База данных инициализирована")

    yield
    await engine.dispose()
    print("🔌 Подключение к БД закрыто")


app = FastAPI(
    title="Personal Expense Tracker API",
    description="Асинхронный трекер доходов и расходов",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])
app.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])