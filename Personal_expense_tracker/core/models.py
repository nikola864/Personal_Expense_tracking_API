from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, DECIMAL, func
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(DeclarativeBase, AsyncAttrs):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    is_income = Column(Boolean, default=False, nullable=False)

    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    user = relationship("User", back_populates="transactions")
    category = relationship(Category, back_populates="transactions")

















