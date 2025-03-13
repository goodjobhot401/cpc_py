import pytest
from cpc.common.const import INIT_USER_DATA


@pytest.mark.parametrize("db_connection", ["favorite"], indirect=True)
@pytest.mark.parametrize("init_repository", ["favorite"], indirect=True)
class Test_Repository_Favorite:
    def _get_favorites(self, cursor, user_id):
        cursor.execute("SELECT * FROM favorite WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def test_01_add_favorite(self, init_repository, db_connection):
        user_id = 1
        symbol_list = INIT_USER_DATA["favorite"]

        init_repository.add_favorite(user_id, symbol_list)

        cursor = db_connection.cursor()
        rows = self._get_favorites(cursor, user_id)

        assert len(rows) == 2
        assert (1, "BTCUSDT", user_id) in rows
        assert (2, "ETHUSDT", user_id) in rows

    def test_02_remove_favorite(self, init_repository, db_connection):
        user_id = 1
        symbol_list = ["BTCUSDT", "ETHUSDT"]

        init_repository.remove_favorite(user_id, symbol_list)

        cursor = db_connection.cursor()
        rows = self._get_favorites(cursor, user_id)

        assert len(rows) == 0
