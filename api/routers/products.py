from fastapi import APIRouter
from datatypes.datatypes import Product
from core.core_functions import get_all_products, add_product

router = APIRouter()


@router.get("/products")
def get_products():
    return get_all_products()


@router.post("/products")
def add_product_(product: Product):
    return add_product(product)


@router.put("/products")
def update_product(product: Product):
    return "Updating product"


@router.delete("/products/{product_it}")
def deleting_product(product_id):
    return "deleting product"
