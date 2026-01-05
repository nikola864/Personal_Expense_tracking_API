from pydantic import BaseModel, Field, AfterValidator, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, Annotated
from decimal import Decimal

def positive_amount(v: float) -> float:
    if v <= 0:
        raise ValueError("Amount must be positive")
    return v

PositiveAmount = Annotated[float, AfterValidator(positive_amount)]

class TransactionCreate(BaseModel):
    amount: PositiveAmount
    description: Optional[str] = Field(None, max_length=200)
    date: Optional[datetime] = None
    user_id: int = Field(gt=0)
    category_id: int = Field(gt=0)

    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    @field_validator("date")
    @classmethod
    def check_date_not_future(cls, v:datetime | None) -> datetime | None:
        if v and v > datetime.now(v.tzinfo):
            raise ValueError("Transaction date cannot be in the future")
        return v


class TransactionResponse(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
