import pytest
from unittest.mock import patch, MagicMock
from cpc.services.symbol import SYMBOL_SERVICE


@pytest.mark.parametrize("query", [None, "BTC"])
@patch("cpc.services.symbol.mexc_market")
class Test_Service_Symbol:
    def test_filter_symbols_01_success(self, mock_mexc_market, query, capsys):
        mock_mexc_market.return_value.get_defaultSymbols.return_value = {
            "data": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "BTCTWD"]
        }

        service = SYMBOL_SERVICE()
        service.filter_symbols(query=query)

        captured = capsys.readouterr().out
        if query is None:
            assert "Alphabetical Index" in captured
            assert "BTCUSDT" in captured
            assert "BTCTWD" in captured
            assert "ETHUSDT" in captured
            assert "BNBUSDT" in captured

        else:
            assert "Query String" in captured
            assert "BTCUSDT" in captured
            assert "BTCTWD" in captured
            assert "ETHUSDT" not in captured
            assert "BNBUSDT" not in captured

    @patch("cpc.services.symbol.Console")
    def test_filter_symbols_02_api_error(self, mock_console, mock_mexc_market, query, capsys):
        mock_console.return_value = MagicMock()
        console = mock_console.return_value

        mock_mexc_market.return_value.get_defaultSymbols.side_effect = Exception(
            "No response from mexc market API")

        service = SYMBOL_SERVICE()
        with pytest.raises(Exception) as e:
            service.filter_symbols(query=query)
        assert "No response from mexc market API" in str(e.value)
        console.print.assert_not_called()
