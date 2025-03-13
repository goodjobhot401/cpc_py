from unittest.mock import patch
from cpc.handlers.favorite_controller import FAVORITE


@patch("cpc.handlers.favorite_controller.FAVORITE_SERVICE")
class Test_Handler_Favorite:
    def test_add_favorite_01_success(self, mock_favorite_service):
        FAVORITE.add_favorite(
            ["BTCUSDT", "ETHUSDT"])

        mock_favorite_service.return_value.add_favorite.assert_called_once_with(
            ["BTCUSDT", "ETHUSDT"])

    def test_add_favorite_02_exception(self, mock_favorite_service, capsys):
        mock_favorite_service.return_value.add_favorite.side_effect = Exception(
            "Exception error")

        result = FAVORITE.add_favorite(
            ["BTCUSDT", "ETHUSDT"])

        assert result is None
        captured = capsys.readouterr()
        assert "Exception error" in captured.out

    def test_remove_favorite_01_success(self, mock_favorite_service):
        mock_favorite_service.return_value.remove_favorite.return_value = "remove_success"

        result = FAVORITE.remove_favorite(
            ["BTCUSDT", "ETHUSDT"])

        assert result == "remove_success"
        mock_favorite_service.return_value.remove_favorite.assert_called_once_with(
            ["BTCUSDT", "ETHUSDT"])

    def test_remove_favorite_02_exception(self, mock_favorite_service, capsys):
        mock_favorite_service.return_value.remove_favorite.side_effect = Exception(
            "remove error")

        result = FAVORITE.remove_favorite(
            ["ETHUSDT", "ETHUSDT"])

        assert result is None
        captured = capsys.readouterr()
        assert "remove error" in captured.out
