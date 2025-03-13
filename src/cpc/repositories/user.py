import sqlite3
from cpc.database.dml.user import USER_SQL
from cpc.common.const import INIT_USER_DATA
from cpc.repositories.asset import ASSET_REPOSITORIES
from cpc.repositories.favorite import FAVORITE_REPOSITORIES


class USER_REPOSITORIES():
    def __init__(self, conn):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self.cursor = conn.cursor()

    def create_default_user(self):
        new_id = self.create_user(INIT_USER_DATA["name"])

        FAVORITE_REPOSITORIES(self.conn).add_favorite(
            new_id, INIT_USER_DATA["favorite"])
        ASSET_REPOSITORIES(self.conn).add_asset(
            new_id, INIT_USER_DATA["asset"])
        return new_id

    def get_users(self):
        cursor = self.cursor
        sql = USER_SQL().get_users()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            return [dict(row) for row in rows]
        return None

    def get_user(self):
        cursor = self.cursor
        sql = USER_SQL()

        user_sql = sql.get_user()
        cursor.execute(user_sql)
        user = dict(cursor.fetchone())
        user_id = user.get("id")

        favorite_sql = sql.get_favorite_sql()
        cursor.execute(favorite_sql, (user_id,))
        favorite_list = cursor.fetchall()
        favorites = list()
        if favorite_list:
            favorites = [dict(row)["symbol"] for row in favorite_list]

        asset_sql = sql.get_asset_sql()
        cursor.execute(asset_sql, (user_id,))
        asset_list = cursor.fetchall()
        asset = list()
        if asset_list:
            asset = [dict(row) for row in asset_list]

        if user_id:
            user["favorite"] = favorites
            user["asset"] = asset
            return user
        return None

    def switch_user(self, user_id=None):
        if not user_id:
            self._auto_switch_user()
            return

        self._remove_all_target()
        sql = USER_SQL().switch_target_user()
        cursor = self.cursor
        cursor.execute(sql, (user_id,))
        self.conn.commit()

        if cursor.rowcount == 0:
            print(f"User id={user_id} does not exist.")
        else:
            print(f"User id={user_id} has been targeted.")
        return

    def create_user(self, name, target=True):
        cursor = self.cursor
        sql = USER_SQL().create_user()
        cursor.execute(sql, (name, 1 if target else 0))
        self.conn.commit()
        new_id = cursor.lastrowid
        print(f"User created: id={new_id}, name={name}, target={target}\n")

        self.switch_user(new_id)
        return new_id

    def update_user(self, user_id, name=None):
        cursor = self.cursor

        fields = []
        values = []
        if name is not None:
            fields.append("name = ?")
            values.append(name)
        if not fields:
            print("No update fields provided.")
            return

        sql = USER_SQL().update_user(fields)
        values.append(user_id)

        cursor.execute(sql, tuple(values))
        self.conn.commit()

        print(f"User id={user_id} updated with: name={name}")
        return

    def remove_user(self, user_id):
        sql = USER_SQL()
        remove_user_sql = sql.remove_user_sql()
        remove_favorite_sql = sql.remove_favorite_sql()
        remove_asset_sql = sql.remove_asset_sql()

        cursor = self.cursor
        cursor.execute(remove_user_sql, (user_id,))
        cursor.execute(remove_favorite_sql, (user_id,))
        cursor.execute(remove_asset_sql, (user_id,))
        self.conn.commit()

        print(f"User id={user_id} removed.\n")

        if not self._is_user_target():
            self._auto_switch_user()
        return

    def _is_user_target(self):
        cursor = self.cursor
        sql = USER_SQL().is_taget_sql()
        cursor.execute(sql)
        users = cursor.fetchall()

        if len(users) == 1:
            return True
        return False

    def _remove_all_target(self):
        cursor = self.cursor
        target_zero_sql = USER_SQL().remove_all_target()
        cursor.execute(target_zero_sql)
        self.conn.commit()
        return

    def _auto_choose_user(self):
        cursor = self.cursor
        auto_choose_sql = USER_SQL().auto_choose_user()
        cursor.execute(auto_choose_sql)
        self.conn.commit()
        return

    def _auto_switch_user(self):
        self._remove_all_target()
        self._auto_choose_user()
        print("Auto switch user done.\n")
        return
