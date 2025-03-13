import copy
import pytest
from unittest.mock import patch
from cpc.services.favorite import FAVORITE_SERVICE


@patch("cpc.services.favorite.USER_REPOSITORIES")
@patch("cpc.services.favorite.FAVORITE_REPOSITORIES")
@pytest.mark.usefixtures("test_user")
class Test_Service_Favorite:
    def test_add_favorite_01_success(self, mock_favorite_repository, mock_user_repository, test_user, capsys):
        user_no_favorite = copy.deepcopy(test_user)
        user_no_favorite["favorite"] = []
        mock_user_repository.return_value.get_user.return_value = user_no_favorite

        service = FAVORITE_SERVICE()
        service.add_favorite(
            ["BTCUSDT", "ETHUSDT"])

        mock_favorite_repository.return_value.add_favorite.assert_called_once_with(test_user["id"], [
            "BTCUSDT", "ETHUSDT"])
        captured = capsys.readouterr().out
        assert "add success" in captured

    def test_add_favorite_02_no_user(self, mock_favorite_repository, mock_user_repository, capsys):
        mock_user_repository.return_value.get_user.return_value = None

        service = FAVORITE_SERVICE()
        service.add_favorite(["BTCUSDT"])

        captured = capsys.readouterr().out
        assert "No user has been targeted." in captured
        mock_favorite_repository.return_value.add_favorite.assert_not_called()

    def test_add_favorite_03_api_invalid_symbol(self, mock_favorite_repository, mock_user_repository, test_user, capsys):
        user_no_favorite = copy.deepcopy(test_user)
        user_no_favorite["favorite"] = []
        mock_user_repository.return_value.get_user.return_value = user_no_favorite

        service = FAVORITE_SERVICE()
        service.add_favorite(
            ["invalidusdt", "btcusdt", "ethusdt"])

        mock_favorite_repository.return_value.add_favorite.assert_called_once_with(test_user["id"], [
            "BTCUSDT", "ETHUSDT"])
        captured = capsys.readouterr().out
        assert "invalid" in captured

    @patch("cpc.services.favorite.mexc_market")
    def test_add_favorite_04_api_error(self, mexc_market, mock_favorite_repository, mock_user_repository, test_user):
        mock_user_repository.return_value.get_user.return_value = test_user

        mexc_market.return_value.get_price.side_effect = Exception(
            "No response from mexc market API:")

        service = FAVORITE_SERVICE()
        with pytest.raises(Exception) as e:
            service.add_favorite(
                ["invalidusdt", "btcusdt", "ethusdt"])
        assert "No response from mexc market API:" in str(e.value)
        mock_favorite_repository.return_value.add_favorite.assert_not_called()

    def test_remove_favorite_01_success(self, mock_favorite_repository, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user

        sevice = FAVORITE_SERVICE()
        sevice.remove_favorite(["BTCUSDT", "ETHUSDT"])

        mock_favorite_repository.return_value.remove_favorite.assert_called_once_with(
            test_user["id"], ["BTCUSDT", "ETHUSDT"])
        captured = capsys.readouterr().out
        assert "remove success" in captured

    def test_remove_favorite_02_not_your_favorite(self, mock_favorite_repository, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user

        sevice = FAVORITE_SERVICE()
        # passing an odd number of parameters
        sevice.remove_favorite(["INVALIDUSDT", "NOTYOURUSDT"])
        captured = capsys.readouterr().out
        assert "not in your favorite list" in captured
