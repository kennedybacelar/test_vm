from typing import List
from datatypes.datatypes import User
from database import sql_connection


def registering_user(user: User) -> bool:
    return sql_connection.inserting_into_table(table_name="users", data=dict(user))


def get_all_users() -> List[User]:
    return sql_connection.selecting_from_table(table_name="users")
