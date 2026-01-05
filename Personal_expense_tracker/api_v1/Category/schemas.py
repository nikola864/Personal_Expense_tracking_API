from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    is_income: bool = False

    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

class CategoryResponse(CategoryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

