import copy
import pytest
from unittest.mock import patch
from cpc.services.asset import ASSET_SERVICE


@patch("cpc.services.asset.USER_REPOSITORIES")
@patch("cpc.services.asset.ASSET_REPOSITORIES")
@pytest.mark.usefixtures("test_user")
class Test_Service_Asset:
    def test_add_asset_01_success(self, mock_asset_repository, mock_user_repository, test_user, capsys):
        user_no_asset = copy.deepcopy(test_user)
        user_no_asset["asset"] = []
        mock_user_repository.return_value.get_user.return_value = user_no_asset

        service = ASSET_SERVICE()
        service.add_asset(
            ["btcusdt", "0.5", "ethusdt", "2.5"])

        mock_asset_repository.return_value.add_asset.assert_called_once_with(test_user["id"], [
            {"symbol": "BTCUSDT", "amount": 0.5},
            {"symbol": "ETHUSDT", "amount": 2.5}
        ])
        captured = capsys.readouterr().out
        assert "add success" in captured

    def test_add_asset_02_no_user(self, mock_asset_repository, mock_user_repository, capsys):
        mock_user_repository.return_value.get_user.return_value = None

        service = ASSET_SERVICE()
        service.add_asset(["BTCUSDT", "0.5"])

        captured = capsys.readouterr().out
        assert "No user has been targeted." in captured
        mock_asset_repository.return_value.add_asset.assert_not_called()

    def test_add_asset_03_api_invalid_symbol(self, mock_asset_repository, mock_user_repository, test_user, capsys):
        user_no_asset = copy.deepcopy(test_user)
        user_no_asset["asset"] = []
        mock_user_repository.return_value.get_user.return_value = user_no_asset

        service = ASSET_SERVICE()
        service.add_asset(
            ["invalidusdt", "1.0", "btcusdt", "0.5", "ethusdt", "2.5"])

        mock_asset_repository.return_value.add_asset.assert_called_once_with(test_user["id"], [
            {"symbol": "BTCUSDT", "amount": 0.5},
            {"symbol": "ETHUSDT", "amount": 2.5}
        ])
        captured = capsys.readouterr().out
        assert "invalid" in captured

    def test_add_asset_04_invalid_param_format(self, mock_asset_repository, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user

        service = ASSET_SERVICE()
        service.add_asset(["btcusdt", "0.5", "ethusdt"])

        captured = capsys.readouterr().out
        assert "Parameter format have to be 'symbol amount'" in captured
        mock_asset_repository.return_value.add_asset.assert_not_called()

    @patch("cpc.services.asset.mexc_market")
    def test_add_asset_05_api_error(self, mexc_market, mock_asset_repository, mock_user_repository, test_user):
        mock_user_repository.return_value.get_user.return_value = test_user

        mexc_market.return_value.get_price.side_effect = Exception(
            "No response from mexc market API:")

        service = ASSET_SERVICE()
        with pytest.raises(Exception) as e:
            service.add_asset(
                ["invalidusdt", "1.0", "btcusdt", "0.5", "ethusdt", "2.5"])
        assert "No response from mexc market API:" in str(e.value)
        mock_asset_repository.return_value.add_asset.assert_not_called()

    def test_update_asset_01_success(self, mock_asset_repository, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user

        sevice = ASSET_SERVICE()
        sevice.update_asset(["BTCUSDT", "3.0", "ETHUSDT", "3.5"])

        mock_asset_repository.return_value.update_asset.assert_called_once_with(test_user["id"], [
            {"symbol": "BTCUSDT", "amount": 3.0},
            {"symbol": "ETHUSDT", "amount": 3.5}
        ])
        captured = capsys.readouterr().out
        assert "update success" in captured

    def test_update_asset_02_invalid_symbol(self, mock_asset_repository, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user

        sevice = ASSET_SERVICE()
        sevice.update_asset(["invalidusdt", "1.0", "BTCUSDT", "2.0"])

        mock_asset_repository.return_value.update_asset.assert_called_once_with(test_user["id"], [
            {"symbol": "BTCUSDT", "amount": 2.0}
        ])
        captured = capsys.readouterr().out
        assert "invalidusdt" in captured

    def test_remove_asset_01_success(self, mock_asset_repository, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user

        sevice = ASSET_SERVICE()
        sevice.remove_asset(["BTCUSDT", "ETHUSDT"])

        mock_asset_repository.return_value.remove_asset.assert_called_once_with(
            test_user["id"], ["BTCUSDT", "ETHUSDT"])
        captured = capsys.readouterr().out
        assert "remove success" in captured

    def test_remove_asset_02_not_your_asset(self, mock_asset_repository, mock_user_repository, test_user, capsys):
        mock_user_repository.return_value.get_user.return_value = test_user

        sevice = ASSET_SERVICE()
        # passing an odd number of parameters
        sevice.remove_asset(["INVALIDUSDT", "NOTYOURUSDT"])
        captured = capsys.readouterr().out
        assert "not in your asset list" in captured
