import sqlite3
from typing import Union, Tuple, Optional
import os


class SQLConnection:
    def __init__(self):
        db_file_name = "my_db"
        # self._reset_db(db_file_name)
        self.con = sqlite3.connect(
            f"file:{db_file_name}?cache=shared",
            uri=True,
            check_same_thread=False,
            isolation_level=None,
            timeout=0.01,
        )
        self.tables = {
            "users": ("username", "password", "balance", "role"),
            "products": ("id", "name", "cost", "amount_available", "seller_id"),
        }
        self.creating_tables()

    def creating_tables(self):
        cur = self.con.cursor()
        for table_name, columns in self.tables.items():
            cur.execute(f"create table if not exists {table_name} {columns}")

    def _reset_db(self, db_file_name):
        if os.path.exists(db_file_name):
            os.remove(db_file_name)

    def _check_if_entry_exists(
        self, table_name: str, reference_column: str, reference_value: Union[int, str]
    ) -> int:
        # Returns 0 if entry not found and 1 if it does
        cur = self.con.cursor()
        return cur.execute(
            f"select exists(select 1 from {table_name} where {reference_column}='{reference_value}');"
        ).fetchone()[0]

    def get_table_names(self):
        return list(self.tables.keys())

    def selecting_from_table(self, table_name: str):
        cur = self.con.cursor()
        cur.execute(f"select * from {table_name}")
        # To return the header (column names), since sqlite doesn't support information_schema
        return [
            dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()
        ]

    def select_single_value_from_table_by_reference(
        self,
        table_name: str,
        column_name: str,
        reference_column: str,
        reference_value: Union[str, int],
    ) -> Tuple[bool, Optional[str]]:

        if self._check_if_entry_exists(
            table_name=table_name,
            reference_column=reference_column,
            reference_value=reference_value,
        ):
            cur = self.con.cursor()
            return (
                True,
                cur.execute(
                    f"select {column_name} from {table_name} where {reference_column}='{reference_value}'"
                ).fetchone()[0],
            )
        return False, None

    def inserting_into_table(self, table_name: str, data: dict):
        cur = self.con.cursor()
        cur.execute(
            f"insert into {table_name}{tuple(data.keys())} values {tuple(data.values())}"
        )
        return True

    def update_existing_entry(
        self,
        table_name: str,
        reference_column: str,
        reference_value: Union[str, int],
        data_to_be_update: dict,
    ):
        if self._check_if_entry_exists(
            table_name=table_name,
            reference_column=reference_column,
            reference_value=reference_value,
        ):
            cur = self.con.cursor()
            columns_vs_values = ",".join(
                [
                    f"{column}='{value}'"
                    for column, value in zip(
                        list(data_to_be_update.keys()), list(data_to_be_update.values())
                    )
                    # To make sure it won't change the primary key
                    if column != reference_column
                ]
            )
            cur.execute(
                f"update {table_name} set {columns_vs_values} where {reference_column}='{reference_value}'"
            )
            return True
        return {
            "message": f"entry {reference_value} does not exist in table {table_name}"
        }

    def delete_entry(
        self, table_name: str, reference_column: str, reference_value: Union[str, int]
    ):
        cur = self.con.cursor()
        cur.execute(
            f"delete from {table_name} where {reference_column}='{reference_value}'"
        )
        return True

    def get_user_balance(self, username: str):
        if self._check_if_entry_exists(
            table_name="users",
            reference_column="username",
            reference_value=username,
        ):
            cur = self.con.cursor()
            cur.execute(f"select balance from users where username = '{username}'")
            return {"user": username, "balance": cur.fetchone()[0]}
        else:
            return {"message": f"User <{username}> not registered"}

    def deposit_into_vendor_machine(self, username: str, deposit_value: int):
        cur = self.con.cursor()
        if self._check_if_entry_exists(
            table_name="users",
            reference_column="username",
            reference_value=username,
        ):

            cur.execute(f"select balance from users where username='{username}';")
            final_balance = int(cur.fetchone()[0]) + deposit_value
            cur.execute(
                f"update users set balance={final_balance} where username='{username}';"
            )
            return self.get_user_balance(username=username)
        else:
            return {"message": f"user {username} not registered in vendor machine"}

    def reset_user_balance(self, username):
        if self._check_if_entry_exists(
            table_name="users",
            reference_column="username",
            reference_value=username,
        ):
            cur = self.con.cursor()
            cur.execute(f"update users set balance={0} where username='{username}';")
            return self.get_user_balance(username=username)
        return {"message": "User not registered in vendor machine"}

    def get_user_by_id(self, username) -> dict:
        if self._check_if_entry_exists(
            table_name="users",
            reference_column="username",
            reference_value=username,
        ):
            cur = self.con.cursor()
            cur.execute(f"select * from users where username='{username}';")
            return [
                dict(zip([d[0] for d in cur.description], row))
                for row in cur.fetchall()
            ][0]
        return {"message": f"user {username} not registered in vendor machine"}

    def _get_product_by_id(self, product_id: str):
        cur = self.con.cursor()
        cur.execute(f"select * from products where id='{product_id}';")
        return [
            dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()
        ][0]

    def buy_product(self, product_id: str, amount_to_be_purchased: int, username: str):
        if not self._check_if_entry_exists(
            table_name="products",
            reference_column="id",
            reference_value=product_id,
        ):
            return False, {"message": f"product {product_id} not registered"}
        product = self._get_product_by_id(product_id)
        if amount_to_be_purchased > int(product["amount_available"]):
            return False, {
                "message": f"Stock not enough - Available quantity: {product['amount_available']}"
            }
        total_cost = int(product["cost"] * amount_to_be_purchased)
        user_balance = self.get_user_balance(username)["balance"]
        if total_cost > int(user_balance):
            return False, {"message": "Insufficient funds"}
        self.update_existing_entry(
            table_name="users",
            reference_column="username",
            reference_value=username,
            data_to_be_update={"balance": int(user_balance) - total_cost},
        )
        self.update_existing_entry(
            table_name="products",
            reference_column="id",
            reference_value=product_id,
            data_to_be_update={
                "amount_available": int(int(product["amount_available"]))
                - amount_to_be_purchased
            },
        )
        self.reset_user_balance(username)
        return True, {"user_change": int(user_balance) - total_cost}

    def delete_from_table(self, table_name: str):
        cur = self.con.cursor()
        cur.execute(f"delete from {table_name}")


sql_connection = SQLConnection()
