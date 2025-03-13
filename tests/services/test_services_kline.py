import pytest
from unittest.mock import patch, MagicMock
from cpc.services.kline import KLINE_SERVICE


@patch("cpc.services.kline.mexc_market")
class Test_Service_Kline:
    def test_get_kline_01_suceess(self, mock_market):
        mock_market.return_value.get_kline.return_value = MagicMock()

        service = KLINE_SERVICE()
        with patch.object(service, "_plot_candlesticks", wraps=service._plot_candlesticks) as mock_plot:
            service.get_kline(symbol="BTCUSDT", interval="1d",
                              limit=30, test=True)
            mock_plot.assert_called_once()
            args, kwargs = mock_plot.call_args
            assert len(args) == 4
            assert args[1] == "BTCUSDT"
            assert args[2] == "1d"
            assert args[3] == True

    def test_get_kline_02_invalid_param(self, mock_market, capsys):
        service = KLINE_SERVICE()

        with patch.object(service, "_plot_candlesticks", wraps=service._plot_candlesticks) as mock_plot:
            service.get_kline("BTCUSDT", "1y", 30)
            mock_plot.assert_not_called()

        captured = capsys.readouterr().out
        assert "1y is valid, --interval only accepts the following values:" in captured

    def test_get_kline_03_api_error(self, mock_market):
        mock_market.return_value.get_kline.side_effect = Exception(
            "No response from mexc market API")

        service = KLINE_SERVICE()
        with pytest.raises(Exception) as e:
            service.get_kline(symbol="BTCUSDT", interval="1d",
                              limit=30, test=True)

        assert "No response from mexc market API" in str(e.value)
