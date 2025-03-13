from unittest.mock import patch
from cpc.handlers.kline_controller import KLINE


@patch("cpc.handlers.kline_controller.KLINE_SERVICE")
class Test_Handler_Kline:
    def test_get_kline_01_success(self, mock_kline_service):
        KLINE.get_kline(
            "BTCUSDT", "1M", 30)

        mock_kline_service.return_value.get_kline.assert_called_once_with(
            "BTCUSDT", "1M", 30)

    def test_get_kline_02_exception(self, mock_kline_service, capsys):
        mock_kline_service.return_value.get_kline.side_effect = Exception(
            "Exception error")

        result = KLINE.get_kline(
            "BTCUSDT", "1M", 30)

        assert result is None
        captured = capsys.readouterr()
        assert "Exception error" in captured.out
