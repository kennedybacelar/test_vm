from fastapi import APIRouter, Request
from datatypes.datatypes import DepositValue
from core.core_functions import (
    get_user_balance,
    deposit_into_vendor_machine,
    reset_user_balance,
)

router = APIRouter()


@router.get("/balance")
def get_user_balance_():
    return get_user_balance(username="kenn.galo")


@router.post("/deposit")
def deposit_value(deposit: DepositValue):
    return deposit_into_vendor_machine(deposit_value=deposit.value)


@router.post("/buy/{product_id}")
def buy_product(product_id):
    return "buying product"


@router.post("/reset")
def reset_user_balance_():
    return reset_user_balance()
