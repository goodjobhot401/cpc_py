from unittest.mock import patch
from cpc.handlers.asset_controller import ASSET


@patch("cpc.handlers.asset_controller.ASSET_SERVICE")
class Test_Handler_Asset:
    def test_add_asset_01_success(self, mock_asset_service):
        ASSET.add_asset(
            ["BTCUSDT", "0.5"])

        mock_asset_service.return_value.add_asset.assert_called_once_with(
            ["BTCUSDT", "0.5"])

    def test_add_asset_02_exception(self, mock_asset_service, capsys):
        mock_asset_service.return_value.add_asset.side_effect = Exception(
            "Exception error")

        result = ASSET.add_asset(
            ["BTCUSDT", "0.5"])

        assert result is None
        captured = capsys.readouterr()
        assert "Exception error" in captured.out

    def test_update_asset_01_success(self, mock_asset_service):
        mock_asset_service.return_value.update_asset.return_value = "update_success"

        result = ASSET.update_asset(
            ["BTCUSDT", "2.0"])

        assert result == "update_success"
        mock_asset_service.return_value.update_asset.assert_called_once_with(
            ["BTCUSDT", "2.0"])

    def test_update_asset_02_exception(self, mock_asset_service, capsys):
        mock_asset_service.return_value.update_asset.side_effect = Exception(
            "update error")

        result = ASSET.update_asset(
            ["BTCUSDT", "1.5"])

        assert result is None
        captured = capsys.readouterr()
        assert "update error" in captured.out

    def test_remove_asset_01_success(self, mock_asset_service):
        mock_asset_service.return_value.remove_asset.return_value = "remove_success"

        result = ASSET.remove_asset(
            ["BTCUSDT", "1.0"])

        assert result == "remove_success"
        mock_asset_service.return_value.remove_asset.assert_called_once_with(
            ["BTCUSDT", "1.0"])

    def test_remove_asset_02_exception(self, mock_asset_service, capsys):
        mock_asset_service.return_value.remove_asset.side_effect = Exception(
            "remove error")

        result = ASSET.remove_asset(
            ["ETHUSDT", "0.2"])

        assert result is None
        captured = capsys.readouterr()
        assert "remove error" in captured.out
