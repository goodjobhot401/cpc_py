import os
import sqlite3
from functools import wraps
from cpc.common.config import DB_PATH
from cpc.database.dml.init import init
from cpc.repositories.user import USER_REPOSITORIES


def init_tables(conn):
    cursor = conn.cursor()
    cursor.execute(init.USER_TABLE_SQL)
    cursor.execute(init.FAVORITE_TABLE_SQL)
    cursor.execute(init.ASSET_TABLE_SQL)
    conn.commit()


def db_connection(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        is_first_time = not os.path.exists(DB_PATH)
        conn = sqlite3.connect(DB_PATH)

        if is_first_time:
            init_tables(conn)
            USER_REPOSITORIES(conn).create_default_user()
            print("Database has been initialized.")

        try:
            return func(self, conn, *args, **kwargs)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.commit()
    return wrapper
