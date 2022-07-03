import sqlite3
from typing import Union, Tuple


class SQLConnection:
    def __init__(self):
        self.con = sqlite3.connect(":memory:", check_same_thread=False)
        self.tables = {
            "users": ("username", "password", "balance", "role"),
            "products": ("id", "name", "cost", "amount_available", "seller_id"),
        }
        self.creating_tables()

    def get_table_names(self):
        return list(self.tables.keys())

    def creating_tables(self):
        cur = self.con.cursor()
        for table_name, columns in self.tables.items():
            cur.execute(f"create table {table_name} {columns}")

    def selecting_from_table(self, table_name: str):
        cur = self.con.cursor()
        cur.execute(f"select * from {table_name}")
        # To return the header (column names), since sqlite doesn't support information_schema
        return [
            dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()
        ]

    def inserting_into_table(self, table_name: str, data: dict):
        cur = self.con.cursor()
        cur.execute(
            f"insert into {table_name}{tuple(data.keys())} values {tuple(data.values())}"
        )
        return True

    def _check_if_entry_exists(
        self, table_name: str, reference_column: str, reference_value: Union[int, str]
    ) -> int:
        # Returns 0 if entry not found and 1 if it does
        cur = self.con.cursor()
        return cur.execute(
            f"select exists(select 1 from {table_name} where {reference_column}='{reference_value}');"
        ).fetchone()[0]

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
                ]
            )
            cur.execute(
                f"update {table_name} set {columns_vs_values} where {reference_column}='{reference_value}'"
            )
            return True
        return {
            "message": f"entry {reference_value} does not exist in table {table_name}"
        }

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
            cur.execute(
                f"insert into users(username, balance) values ('{username}', '{deposit_value}')"
            )
            return self.get_user_balance(username=username)

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

    def _getting_product_quantity(self, product_id: str):
        pass

    def buy_product(self, product_id: str, amount_to_be_purchased: int):
        pass


sql_connection = SQLConnection()
