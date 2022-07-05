from typing import List, Tuple, Union, Optional
import bcrypt
from datatypes.datatypes import User, Product, ProductPurchase
from database import sql_connection


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


def _get_user_role(username: str) -> Tuple[bool, Optional[str]]:
    return sql_connection.select_single_value_from_table_by_reference(
        table_name="users",
        column_name="role",
        reference_column="username",
        reference_value=username,
    )


def _get_product_seller_id(product_id: str) -> Tuple[bool, Optional[str]]:
    return sql_connection.select_single_value_from_table_by_reference(
        table_name="products",
        column_name="seller_id",
        reference_column="id",
        reference_value=product_id,
    )


def registering_user(user: User) -> bool:
    return sql_connection.inserting_into_table(table_name="users", data=dict(user))


def get_all_users() -> List[User]:
    return sql_connection.selecting_from_table(table_name="users")


def get_all_products() -> List[Product]:
    return sql_connection.selecting_from_table(table_name="products")


def add_product(product: Product, username: str) -> bool:
    _, user_role = _get_user_role(username)
    if user_role == "seller":
        product.seller_id = username
        return sql_connection.inserting_into_table(
            table_name="products", data=dict(product)
        )
    return {"message": "user should be seller to register products"}


def update_product(
    product_id: str, product: Product, username: str
) -> Union[bool, dict]:
    _, product_seller_id = _get_product_seller_id(product_id)
    if product_seller_id == username:
        return sql_connection.update_existing_entry(
            table_name="products",
            reference_column="id",
            reference_value=product_id,
            data_to_be_update=dict(product),
        )
    return {
        "message": "username authenticated different of seller id who created the product"
    }


def delete_product(product_id: str, username: str) -> bool:
    _, product_seller_id = _get_product_seller_id(product_id)
    if product_seller_id == username:
        return sql_connection.delete_entry(
            table_name="products", reference_column="id", reference_value=product_id
        )
    return {
        "message": "username authenticated different of seller id who created the product"
    }


def get_user_balance(username: str) -> dict:
    return sql_connection.get_user_balance(username=username)


def get_my_user_info(username: str) -> dict:
    return sql_connection.get_user_by_id(username)


def deposit_into_vendor_machine(deposit_value: int, username: str) -> dict:
    return sql_connection.deposit_into_vendor_machine(
        username=username, deposit_value=deposit_value
    )


def reset_user_balance(username: str) -> dict:
    return sql_connection.reset_user_balance(username=username)


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


def buy_product(product_purchase: ProductPurchase, username: str):
    _, user_role = _get_user_role(username)
    if user_role == "buyer":
        return sql_connection.buy_product(
            product_id=product_purchase.product_id,
            amount_to_be_purchased=product_purchase.amount,
            username=username,
        )
    return {"message": "User needs to be a buyer in order to perform this operation"}
