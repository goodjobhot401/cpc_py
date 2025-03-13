import pytest
from unittest.mock import patch
from cpc.handlers.price_controller import PRICE


@patch("cpc.handlers.price_controller.PRICE_SERVICE")
@pytest.mark.usefixtures("test_user")
class Test_Handler_Price:
    def test_get_price_detail_01_success(self, mock_price_service, test_user):
        symbols = test_user["favorite"]
        PRICE.get_price_detail(symbols)

        mock_price_service.return_value.get_price_detail.assert_called_once_with(
            symbols)

    def test_get_price_detail_02_exception(self, mock_price_service, test_user, capsys):
        symbols = test_user["favorite"]
        mock_price_service.return_value.get_price_detail.side_effect = Exception(
            "Exception error")

        result = PRICE.get_price_detail(symbols)

        assert result is None
        captured = capsys.readouterr().out
        assert "Exception error" in captured
