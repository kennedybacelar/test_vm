from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datatypes.datatypes import Product, ProductUpdate
from core.core_functions import (
    get_all_products,
    add_product,
    is_authentication_successful,
    update_product,
    delete_product,
)

router = APIRouter()
security = HTTPBasic()


@router.get("/products")
def get_products(credentials: HTTPBasicCredentials = Depends(security)):
    return get_all_products()


@router.post("/products")
def add_product_(
    product: Product, credentials: HTTPBasicCredentials = Depends(security)
):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return add_product(product=product, username=credentials.username)
    return {"message": "Authentication failure"}


@router.put("/products/update/{product_id}")
def update_product_(
    product_id: str,
    product: ProductUpdate,
    credentials: HTTPBasicCredentials = Depends(security),
):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return update_product(
            product_id=product_id, product=product, username=credentials.username
        )
    return {"message": "Authentication failure"}


@router.delete("/products/delete/{product_id}")
def deleting_product(product_id, credentials: HTTPBasicCredentials = Depends(security)):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return delete_product(product_id=product_id, username=credentials.username)
    return {"message": "Authentication failure"}
