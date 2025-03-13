import pytest
from cpc.common.const import INIT_USER_DATA


@pytest.mark.parametrize("db_connection", ["asset"], indirect=True)
@pytest.mark.parametrize("init_repository", ["asset"], indirect=True)
class Test_Repository_Asset:
    def _get_assets(self, cursor, user_id):
        cursor.execute("SELECT * FROM asset WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def test_01_add_asset(self, init_repository, db_connection):
        user_id = 1
        symbol_list = INIT_USER_DATA["asset"]

        init_repository.add_asset(user_id, symbol_list)

        cursor = db_connection.cursor()
        rows = self._get_assets(cursor, user_id)

        assert len(rows) == 2
        assert (1, "BTCUSDT", 0.5, user_id) in rows
        assert (2, "ETHUSDT", 50.0, user_id) in rows

    def test_02_update_asset(self, init_repository, db_connection):
        user_id = 1
        init_repository.add_asset(user_id, INIT_USER_DATA["asset"])

        update_symbol_list = [
            {"symbol": "BTCUSDT", "amount": 1.5},
            {"symbol": "ETHUSDT", "amount": 2.5}
        ]

        init_repository.update_asset(user_id, update_symbol_list)

        cursor = db_connection.cursor()
        rows = self._get_assets(cursor, user_id)

        assert len(rows) == 2
        assert (1, "BTCUSDT", 1.5, user_id) in rows
        assert (2, "ETHUSDT", 2.5, user_id) in rows

    def test_remove_asset_01(self, init_repository, db_connection):
        user_id = 1
        symbol_list = ["BTCUSDT", "ETHUSDT"]

        init_repository.remove_asset(user_id, symbol_list)

        cursor = db_connection.cursor()
        rows = self._get_assets(cursor, user_id)

        assert len(rows) == 0
