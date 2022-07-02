from fastapi import APIRouter
from datatypes.datatypes import Product

router = APIRouter()


@router.get("/products")
def get_products():
    return "products"


@router.post("/products")
def add_product(product: Product):
    return "adding product"


@router.put("/products")
def update_product(product: Product):
    return "Updating product"


@router.delete("/products/{product_it}")
def deleting_product(product_id):
    return "deleting product"
