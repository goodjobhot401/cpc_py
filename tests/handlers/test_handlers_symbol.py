import pytest
from unittest.mock import patch
from cpc.handlers.symbol_controller import SYMBOL


@patch("cpc.handlers.symbol_controller.SYMBOL_SERVICE")
@pytest.mark.usefixtures("test_user")
class Test_Handler_Symbol:
    def test_filter_symbols_01_success(self, mock_symbol_service, test_user):
        symbols = test_user["favorite"]
        SYMBOL.filter_symbols(symbols)

        mock_symbol_service.return_value.filter_symbols.assert_called_once_with(
            symbols)

    def test_filter_symbols_02_exception(self, mock_symbol_service, test_user, capsys):
        symbols = test_user["favorite"]
        mock_symbol_service.return_value.filter_symbols.side_effect = Exception(
            "Exception error")

        result = SYMBOL.filter_symbols(symbols)

        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured
