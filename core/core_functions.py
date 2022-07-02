from typing import List
from datatypes.datatypes import User, Product
from database import sql_connection


def registering_user(user: User) -> bool:
    return sql_connection.inserting_into_table(table_name="users", data=dict(user))


def get_all_users() -> List[User]:
    return sql_connection.selecting_from_table(table_name="users")


def get_all_products() -> List[Product]:
    return sql_connection.selecting_from_table(table_name="products")


def add_product(product: Product) -> bool:
    return sql_connection.inserting_into_table(
        table_name="products", data=dict(product)
    )
