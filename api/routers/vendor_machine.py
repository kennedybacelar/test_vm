from fastapi import APIRouter, Request
from datatypes.datatypes import DepositValue

router = APIRouter()


@router.get("/balance")
def get_user_balance():
    return "user balance"


@router.post("/deposit")
def deposit_value(deposit_value: DepositValue):
    return "depositing value"


@router.post("/buy/{product_id}")
def buy_product(product_id):
    return "buying product"


@router.post("/reset")
def reset_user_balance():
    return "reset user balance"
