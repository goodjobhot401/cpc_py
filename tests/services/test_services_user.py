import pytest
from unittest.mock import patch, MagicMock
from cpc.services.user import USER_SERVICE


@patch("cpc.services.user.USER_REPOSITORIES")
@pytest.mark.usefixtures("test_user")
class Test_Service_User:
    def test_create_default_user_01_success(self, mock_user_repository):
        service = USER_SERVICE()
        service.create_default_user()
        mock_user_repository.return_value.create_default_user.assert_called_once_with()

    def test_get_users_01_success(self, mock_user_repository, capsys):
        mock_user_repository.return_value.get_users.return_value = [
            {"id": 1, "name": "test_user_1", "target": False},
            {"id": 2, "name": "test_user_2", "target": True}
        ]

        service = USER_SERVICE()
        service.get_users()

        captured = capsys.readouterr().out
        assert "test_user_1" in captured
        assert "test_user_2" in captured
        assert "False" in captured
        assert "True" in captured

    def test_get_user_01_print_table_true(self, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user
        test_user["target"] = True

        service = USER_SERVICE()
        service.get_user(print_table=True)

        captured = capsys.readouterr().out
        assert "ID" in captured
        assert "Name" in captured
        assert "Favorite" in captured
        assert "Asset" in captured
        assert "Target" in captured

    def test_get_user_02_print_table_false(self, mock_user_repository, test_user):
        mock_user_repository.return_value.get_user.return_value = test_user

        service = USER_SERVICE()
        data = service.get_user(print_table=False)

        assert test_user["name"] == data["name"]
        assert test_user["favorite"] == data["favorite"]
        assert test_user["asset"] == data["asset"]

    def test_switch_user_01_success(self, mock_user_repository):
        service = USER_SERVICE()
        service.switch_user(1)

        mock_user_repository.return_value.switch_user.assert_called_once_with(
            1)

    def test_switch_user_02_wrong_param(self, mock_user_repository):
        service = USER_SERVICE()
        with pytest.raises(Exception) as e:
            service.switch_user("Tom")

        assert "Parameter 'user_id' have to be an integer" in str(e.value)
        mock_user_repository.return_value.switch_user.assert_not_called()

    def test_create_user_01_name_with_space_success(self, mock_user_repository):
        service = USER_SERVICE()
        service.create_user(["Tom", "Yung"])

        mock_user_repository.return_value.create_user.assert_called_once_with(
            "Tom Yung")

    def test_create_user_02_name_with_dash_success(self, mock_user_repository):
        service = USER_SERVICE()
        service.create_user(["Tom_yung"])

        mock_user_repository.return_value.create_user.assert_called_once_with(
            "Tom_yung")

    def test_update_user_01_name_with_space_success(self, mock_user_repository):
        service = USER_SERVICE()
        service.update_user(2, ["Tom", "Yung"])

        mock_user_repository.return_value.update_user.assert_called_once_with(
            2,
            "Tom Yung")

    def test_update_user_02_name_with_dash_success(self, mock_user_repository):
        service = USER_SERVICE()
        service.update_user(2, ["Tom_yung"])

        mock_user_repository.return_value.update_user.assert_called_once_with(
            2,
            "Tom_yung")

    def test_update_user_03_wrong_param_format(self, mock_user_repository):
        service = USER_SERVICE()
        with pytest.raises(Exception) as e:
            service.update_user(["Tom_yung"], 2)

        assert "Parameter format have to be 'user_id name'" in str(e.value)
        mock_user_repository.return_value.update_user.assert_not_called()

    def test_remove_user_01_success(self, mock_user_repository):
        service = USER_SERVICE()
        service.remove_user(2)

        mock_user_repository.return_value.remove_user.assert_called_once_with(
            2)

    def test_remove_user_02_wrong_param(self, mock_user_repository):
        service = USER_SERVICE()
        with pytest.raises(Exception) as e:
            service.remove_user("Tom")

        assert "Parameter have to be an integer" in str(e.value)
        mock_user_repository.return_value.remove_user.assert_not_called()

    def test_get_position_ration_01_success(self, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user

        service = USER_SERVICE()
        service.get_position_ratio()

        captured = capsys.readouterr().out
        assert "Symbol" in captured
        assert "Amount" in captured
        assert "Latest Price" in captured
        assert "Market Value" in captured
        assert "Percentage" in captured

    @patch("cpc.services.user.Console")
    @patch("cpc.services.user.mexc_market")
    def test_get_position_ration_02_api_error(self, mock_market, mock_console, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user
        mock_console.return_value = MagicMock()
        console = mock_console.return_value

        mock_market_instance = MagicMock()
        mock_market.return_value = mock_market_instance

        mock_market_instance.get_price.side_effect = Exception(
            "No response from mexc market API")

        service = USER_SERVICE()
        with pytest.raises(Exception) as e:
            service.get_position_ratio()

        assert "No response from mexc market API" in str(e.value)
        console.print.assert_not_called()
