from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)

    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

class UserResponse(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

