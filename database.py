import sqlite3


class SQLConnection:
    def __init__(self):
        self.con = sqlite3.connect(":memory:", check_same_thread=False)
        self.tables = {
            "users": ("username", "password", "balance", "role"),
            "products": ("name", "cost", "amount_available", "seller_id"),
        }
        self.creating_tables()

    def creating_tables(self):
        cur = self.con.cursor()
        for table_name, columns in self.tables.items():
            cur.execute(f"create table {table_name} {columns}")

    def selecting_from_table(self, table_name: str):
        cur = self.con.cursor()
        cur.execute(f"select * from {table_name}")
        return cur.fetchall()

    def inserting_into_table(self, table_name: str, data: dict):
        cur = self.con.cursor()
        cur.execute(
            f"insert into {table_name}{tuple(data.keys())} values {tuple(data.values())}"
        )
        return True


sql_connection = SQLConnection()
