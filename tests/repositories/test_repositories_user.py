import pytest
from unittest.mock import patch
from cpc.common.const import INIT_USER_DATA


@pytest.mark.parametrize("db_connection", ["user"], indirect=True)
@pytest.mark.parametrize("init_repository", ["user"], indirect=True)
class Test_Repository_User:
    def _get_user_by_id(self, cursor, user_id):
        cursor.execute(
            "SELECT name, target FROM user WHERE id = ?", (user_id,))
        return cursor.fetchall()

    def _get_favorite_by_id(self, cursor, user_id):
        cursor.execute(
            "SELECT symbol FROM favorite WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def _get_asset_by_id(self, cursor, user_id):
        cursor.execute(
            "SELECT symbol, amount FROM asset WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def test_01_create_default_user(self, init_repository, db_connection):
        user_id = init_repository.create_default_user()

        cursor = db_connection.cursor()
        user_rows = self._get_user_by_id(cursor, user_id)
        favorite_rows = self._get_favorite_by_id(cursor, user_id)
        asset_rows = self._get_asset_by_id(cursor, user_id)

        for name in user_rows:
            assert str(name[0]) in INIT_USER_DATA["name"]

        for favorite in favorite_rows:
            assert str(favorite[0]) in INIT_USER_DATA["favorite"]

        for asset in asset_rows:
            assert {
                "symbol": asset[0],
                "amount": float(asset[1])
            } in INIT_USER_DATA["asset"]

    def test_02_get_users(self, init_repository, db_connection):
        user1_id = init_repository.create_default_user()
        user2_id = init_repository.create_default_user()

        users = init_repository.get_users()

        for user in users:
            assert user["id"] in [user1_id, user2_id]

    def test_03_get_user(self, init_repository, db_connection):
        init_repository.create_default_user()
        user = init_repository.get_user()

        assert user["name"] == INIT_USER_DATA["name"]
        assert user["favorite"] == INIT_USER_DATA["favorite"]
        assert user["asset"] == INIT_USER_DATA["asset"]

    def test_04_switch_user(self, init_repository, db_connection):
        cursor = db_connection.cursor()

        user1_id = init_repository.create_user("test_user_1")
        user2_id = init_repository.create_user("test_user_2")

        assert self._get_user_by_id(cursor, user1_id)[0]["target"] == False
        assert self._get_user_by_id(cursor, user2_id)[0]["target"] == True

        init_repository.switch_user(user1_id)
        user1_target, user2_target = (
            self._get_user_by_id(cursor, user1_id)[0]["target"],
            self._get_user_by_id(cursor, user2_id)[0]["target"],
        )
        assert user1_target == True
        assert user2_target == False

    def test_05_create_user(self, init_repository, db_connection):
        name = INIT_USER_DATA["name"]
        user_id = init_repository.create_user(name)

        cursor = db_connection.cursor()
        rows = self._get_user_by_id(cursor, user_id)

        for row in rows:
            assert str(row[0]) in INIT_USER_DATA["name"]

    def test_06_update_user(self, init_repository, db_connection):
        user_id = init_repository.create_default_user()
        init_repository.update_user(user_id, "test_user")

        cursor = db_connection.cursor()
        rows = self._get_user_by_id(cursor, user_id)

        assert rows[0]["name"] == "test_user"

    def test_07_remove_user(self, init_repository, db_connection):
        user1_id = init_repository.create_default_user()
        user2_id = init_repository.create_default_user()

        init_repository.remove_user(user2_id)
        rows = init_repository.get_users()

        assert len(rows) == 1
        assert rows[0]["id"] == 1

    def test_08_is_user_target(self, init_repository, db_connection):
        with patch.object(init_repository, "_is_user_target", return_value=False) as mock_is_user_target:
            user1_id = init_repository.create_default_user()
            user2_id = init_repository.create_default_user()

            init_repository.remove_user(user2_id)
            mock_is_user_target.assert_called_once()

    def test_09_remove_all_target(self, init_repository, db_connection):
        with patch.object(init_repository, "_remove_all_target") as mock_remove_all_target:
            init_repository.create_default_user()
            mock_remove_all_target.assert_called_once()

    def test_11_auto_choose_user(self, init_repository, db_connection):
        with patch.object(init_repository, "_auto_choose_user") as mock_auto_choose_user:
            user1_id = init_repository.create_default_user()
            user2_id = init_repository.create_default_user()

            init_repository.remove_user(user2_id)
            mock_auto_choose_user.assert_called_once()

    def test_12_auto_switch_user(self, init_repository, db_connection):
        with patch.object(init_repository, "_auto_switch_user") as mock_auto_switch_user:
            user1_id = init_repository.create_default_user()
            user2_id = init_repository.create_default_user()

            init_repository.remove_user(user2_id)
            mock_auto_switch_user.assert_called_once()
