import pytest
from unittest.mock import patch, MagicMock
from cpc.handlers.user_controller import USER


@patch("cpc.handlers.user_controller.USER_SERVICE")
@pytest.mark.usefixtures("test_user")
class Test_Handler_User:
    def test_create_default_user_01_success(self, mock_user_service):
        USER.create_default_user()

        mock_user_service.return_value.create_default_user.assert_called_once_with()

    def test_create_default_user_02_exception(self, mock_user_service, capsys):
        mock_user_service.return_value.create_default_user.side_effect = Exception(
            "Exception error")

        result = USER.create_default_user()

        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured

    def test_get_users_01_success(self, mock_user_service):
        USER.get_users()

        mock_user_service.return_value.get_users.assert_called_once_with()

    def test_get_users_02_exception(self, mock_user_service, capsys):
        mock_user_service.return_value.get_users.side_effect = Exception(
            "Exception error")

        result = USER.get_users()

        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured

    def test_get_user_01_print_table_is_none(self, mock_user_service):
        print_table = None
        USER.get_user(print_table)
        mock_user_service.return_value.get_user.assert_called_once_with(
            print_table)

    @patch("cpc.services.user.Console")
    def test_get_user_02_print_table_is_true(self, mock_console, mock_user_service):
        print_table = True

        mock_console.return_value = MagicMock()
        console = mock_console.return_value

        result = USER.get_user(print_table)
        assert result is not None
        mock_user_service.return_value.get_user.assert_called_once_with(
            print_table)
        console.print.assert_not_called()

    def test_get_user_03_exception(self, mock_user_service, capsys):
        print_table = None
        mock_user_service.return_value.get_user.side_effect = Exception(
            "Exception error")

        result = USER.get_user(print_table)
        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured

    def test_switch_user_01_success(self, mock_user_service):
        user_id = 1
        USER.switch_user(user_id)
        mock_user_service.return_value.switch_user.assert_called_once_with(
            user_id)

    def test_switch_user_02_user_id_is_none(self, mock_user_service):
        user_id = None
        USER.switch_user()
        mock_user_service.return_value.switch_user.assert_called_once_with(
            user_id)

    def test_switch_user_03_exception(self, mock_user_service, capsys):
        mock_user_service.return_value.switch_user.side_effect = Exception(
            "Exception error")

        result = USER.switch_user()

        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured

    def test_create_user_01_success(self, mock_user_service):
        name = ["test_user"]
        USER.create_user(name)
        mock_user_service.return_value.create_user.assert_called_once_with(
            name)

    def test_create_user_02_create_default_user(self, mock_user_service):
        name = ["-1"]
        USER.create_user(name)
        mock_user_service.return_value.create_default_user.assert_called_once_with()

    def test_create_user_03_exception(self, mock_user_service, capsys):
        name = ["test_user"]
        mock_user_service.return_value.create_user.side_effect = Exception(
            "Exception error")

        result = USER.create_user(name)

        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured

    def test_update_user_01_success(self, mock_user_service):
        user_id = 1
        name = ["test_user"]
        USER.update_user(user_id, name)
        mock_user_service.return_value.update_user.assert_called_once_with(
            user_id, name)

    def test_update_user_02_exception(self, mock_user_service, capsys):
        user_id = 1
        name = ["test_user"]

        mock_user_service.return_value.update_user.side_effect = Exception(
            "Exception error")

        result = USER.update_user(user_id, name)

        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured

    def test_remove_user_01_success(self, mock_user_service):
        user_id = 1
        USER.remove_user(user_id)
        mock_user_service.return_value.remove_user.assert_called_once_with(
            user_id)

    def test_remove_user_02_exception(self, mock_user_service, capsys):
        user_id = 1
        mock_user_service.return_value.remove_user.side_effect = Exception(
            "Exception error")

        result = USER.remove_user(user_id)
        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured

    def test_get_position_ratio_01_success(self, mock_user_service):
        sort = "value"
        reverse = True
        USER.get_position_ratio(sort, reverse)
        mock_user_service.return_value.get_position_ratio.assert_called_once_with(
            sort, reverse)

    def test_get_position_ratio_02_exception(self, mock_user_service, capsys):
        sort = "value"
        reverse = True

        mock_user_service.return_value.get_position_ratio.side_effect = Exception(
            "Exception error")

        result = USER.get_position_ratio(sort, reverse)
        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured
