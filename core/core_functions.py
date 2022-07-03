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


def update_product(product: Product) -> bool:
    product_id = product.id
    product_data = dict(product)
    del product_data["id"]
    return sql_connection.update_existing_entry(
        table_name="products",
        reference_column="id",
        reference_value=product_id,
        data_to_be_update=product_data,
    )


def get_user_balance(username: str) -> dict:
    return sql_connection.get_user_balance(username=username)


def deposit_into_vendor_machine(deposit_value: int) -> dict:
    return sql_connection.deposit_into_vendor_machine(
        username="kenn.galo", deposit_value=deposit_value
    )


def reset_user_balance() -> dict:
    return sql_connection.reset_user_balance(username="kenn.galo")


def buy_product():
    pass


def is_user_authenticated():
    pass


def get_user_role():
    pass
