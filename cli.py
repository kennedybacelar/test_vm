from database import sql_connection
import pprint


def get_table_names():
    pprint.pprint(sql_connection.get_table_names())


if __name__ == "__main__":
    get_table_names()
