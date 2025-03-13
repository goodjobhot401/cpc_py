import sqlite3
from cpc.database.dml.asset import ASSET_SQL


class ASSET_REPOSITORIES():
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def add_asset(self, user_id, symbol_list):
        cursor = self.cursor

        data = []
        for item in symbol_list:
            symbol = item["symbol"]
            amount = float(item["amount"])
            data.append((symbol, amount, user_id))

        sql = ASSET_SQL().add_asset_sql()
        cursor.executemany(sql, data)
        self.conn.commit()
        return

    def update_asset(self, user_id, symbol_list):
        cursor = self.cursor

        data = []
        for item in symbol_list:
            amount = float(item["amount"])
            symbol = item["symbol"]
            data.append((amount, symbol, user_id))

        sql = ASSET_SQL().update_asset_sql()
        cursor.executemany(sql, data)
        self.conn.commit()
        return

    def remove_asset(self, user_id, symbol_list):
        cursor = self.cursor

        data = []
        for symbol in symbol_list:
            data.append((symbol, user_id))

        sql = ASSET_SQL().remove_asset_sql()
        cursor.executemany(sql, data)
        self.conn.commit()
        return
