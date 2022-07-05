from typing import List, Tuple, Union
import bcrypt
from datatypes.datatypes import User, Product
from database import sql_connection
from .authentication import get_settings


def is_authentication_successful(username: Union[str, int], password: str):

    username = username.replace("\n", "")
    password = password.replace("\n", "")
    # in a real application this is supposed to stay in a local file like .secrets.env
    (
        found_entry,
        stored_password_hash,
    ) = sql_connection.select_single_value_from_table_by_reference(
        table_name="users",
        column_name="password",
        reference_column="username",
        reference_value=username,
    )

    if found_entry:
        return bcrypt.checkpw(
            password.encode("utf-8"), stored_password_hash.encode("utf-8")
        )
    return False


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


def update_product(product_id: str, product: Product) -> bool:
    product_id = product_id
    return sql_connection.update_existing_entry(
        table_name="products",
        reference_column="id",
        reference_value=product_id,
        data_to_be_update=dict(product),
    )


def delete_product(product_id: str) -> bool:
    return sql_connection.delete_entry(
        table_name="products", reference_column="id", reference_value=product_id
    )


def get_user_balance(username: str) -> dict:
    return sql_connection.get_user_balance(username=username)


def deposit_into_vendor_machine(deposit_value: int) -> dict:
    return sql_connection.deposit_into_vendor_machine(
        username="kenn.galo", deposit_value=deposit_value
    )


def reset_user_balance() -> dict:
    return sql_connection.reset_user_balance(username="kenn.galo")


def update_user(username: str, user: User):
    return sql_connection.update_existing_entry(
        table_name="users",
        reference_column="username",
        reference_value=username,
        data_to_be_update=dict(user),
    )


def delete_user(username: str):
    return sql_connection.delete_entry(
        table_name="users", reference_column="username", reference_value=username
    )


def _get_user_role(username: str) -> Tuple[bool, str]:
    return sql_connection.select_single_value_from_table_by_reference(
        table_name="users",
        column_name="role",
        reference_column="username",
        reference_value=username,
    )


def buy_product(product_id):
    _, user_role = _get_user_role(username="yan.bacelar")
    if user_role == "buyer":
        return "eh comprador"
    elif user_role == "seller":
        return "vendedor"


def is_user_authenticated():
    pass


def get_user_role():
    pass
