from enum import Enum
from pydantic import BaseModel, validator


class UserRole(Enum):
    buyer = "buyer"
    seller = "seller"


class DepositValue(BaseModel):
    deposit_value: int

    @validator("deposit_value")
    def must_be_in_following_coin_values(cls, v):
        allowed_coin_values = [5, 10, 20, 50, 100]
        if v not in allowed_coin_values:
            raise ValueError(
                f"The coin value must be one of the options in the following list  {allowed_coin_values}"
            )


class User(BaseModel):
    username: str
    password: str
    balance: int = 0
    role: UserRole


class Product(BaseModel):
    name: str
    cost: int
    amount_available: int
    seller_id: int

    @validator("cost")
    def must_be_multiple_of_5(cls, v):
        if not v % 5 == 0:
            raise ValueError("Should be multiple of 5")
