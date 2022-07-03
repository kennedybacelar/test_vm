import sqlite3
from typing import Union


class SQLConnection:
    def __init__(self):
        self.con = sqlite3.connect(":memory:", check_same_thread=False)
        self.tables = {
            "users": ("username", "password", "balance", "role"),
            "products": ("name", "cost", "amount_available", "seller_id"),
            "vendor_machine": ("username", "balance"),
        }
        self.creating_tables()

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

    def get_user_balance(self, username: str):
        cur = self.con.cursor()
        cur.execute(f"select balance from vendor_machine where username = '{username}'")
        return cur.fetchone()

    def _check_if_entry_exists(
        self, table_name: str, reference_column: str, reference_value: Union[int, str]
    ) -> int:
        # Returns 0 if entry not found and 1 if it does
        cur = self.con.cursor()
        return cur.execute(
            f"select exists(select 1 from {table_name} where {reference_column}='{reference_value}');"
        ).fetchone()[0]

    def deposit_into_vendor_machine(self, username: str, deposit_value: int):
        cur = self.con.cursor()
        if self._check_if_entry_exists(
            table_name="vendor_machine",
            reference_column="username",
            reference_value=username,
        ):

            cur.execute(
                f"select balance from vendor_machine where username='{username}';"
            )
            final_balance = int(cur.fetchone()[0]) + deposit_value
            cur.execute(
                f"update vendor_machine set balance={final_balance} where username='{username}';"
            )
            return final_balance  # To be amended and inserted into db
        else:
            cur.execute(
                f"insert into vendor_machine(username, balance) values ('{username}', '{deposit_value}')"
            )
            return deposit_value

    def reset_user_balance(self, username):
        if self._check_if_entry_exists(
            table_name="vendor_machine",
            reference_column="username",
            reference_value=username,
        ):
            cur = self.con.cursor()
            cur.execute(
                f"update vendor_machine set balance={0} where username='{username}';"
            )
        return {"message": "User not registered in vendor machine"}


sql_connection = SQLConnection()
