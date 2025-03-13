import sqlite3
from cpc.database.dml.favorite import FAVORITE_SQL


class FAVORITE_REPOSITORIES():
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def add_favorite(self, user_id, symbol_list):
        cursor = self.cursor

        data = []
        for symbol in symbol_list:
            data.append((symbol, user_id))

        add_favorite_sql = FAVORITE_SQL().add_favorite_sql()
        cursor.executemany(add_favorite_sql, data)
        self.conn.commit()
        return

    def remove_favorite(self, user_id, symbol_list):
        cursor = self.conn.cursor()

        data = []
        for symbol in symbol_list:
            data.append((symbol, user_id))

        remove_favorite_sql = FAVORITE_SQL().remove_favorite_sql()
        cursor.executemany(remove_favorite_sql, data)
        self.conn.commit()
        return
