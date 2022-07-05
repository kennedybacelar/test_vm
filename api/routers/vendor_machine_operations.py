from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datatypes.datatypes import DepositValue, ProductPurchase
from core.core_functions import (
    get_user_balance,
    deposit_into_vendor_machine,
    is_authentication_successful,
    reset_user_balance,
    buy_product,
)

router = APIRouter()
security = HTTPBasic()


@router.get("/balance")
def get_user_balance_(credentials: HTTPBasicCredentials = Depends(security)):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return get_user_balance(username=credentials.username)
    return {"message": "Authentication failure"}


@router.post("/deposit")
def deposit_value(
    deposit: DepositValue, credentials: HTTPBasicCredentials = Depends(security)
):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return deposit_into_vendor_machine(
            deposit_value=deposit.value, username=credentials.username
        )
    return {"message": "Authentication failure"}


@router.post("/buy")
def buy_product_(
    product_purchase: ProductPurchase,
    credentials: HTTPBasicCredentials = Depends(security),
):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return buy_product(
            product_purchase=product_purchase, username=credentials.username
        )
    return {"message": "Authentication failure"}


@router.post("/reset-balance")
def reset_user_balance_(credentials: HTTPBasicCredentials = Depends(security)):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return reset_user_balance(username=credentials.username)
    return {"message": "Authentication failure"}
