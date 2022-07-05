from fastapi import APIRouter
from datatypes.datatypes import Product
from core.core_functions import (
    get_all_products,
    add_product,
    update_product,
    delete_product,
)

router = APIRouter()


@router.get("/products")
def get_products():
    return get_all_products()


@router.post("/products")
def add_product_(product: Product):
    return add_product(product)


@router.put("/products/update/{product_id}")
def update_product_(product_id: str, product: Product):
    return update_product(product_id=product_id, product=product)


@router.delete("/products/delete/{product_id}")
def deleting_product(product_id):
    return delete_product(product_id)
