import pytest
from unittest.mock import patch, MagicMock
from cpc.services.price import PRICE_SERVICE


@patch("cpc.services.price.Console")
@pytest.mark.usefixtures("test_user")
class Test_Service_Price:
    @patch("cpc.services.price.Table")
    def test_get_price_detail_01_success(self, mock_table, mock_console, test_user):
        mock_console.return_value = MagicMock()
        mock_table.return_value = MagicMock()
        console = mock_console.return_value
        table = mock_table.return_value

        symbols = test_user["favorite"]
        service = PRICE_SERVICE()
        service.get_price_detail(symbols)

        console.print.assert_called_once_with(table)

    def test_get_price_detail_02_invalid_param(self, mock_console):
        mock_console.return_value = MagicMock()
        console = mock_console.return_value

        service = PRICE_SERVICE()
        with pytest.raises(Exception) as e:
            service.get_price_detail(
                ["SOL"])

        assert "'SOL' is invalid." in str(e.value)
        console.print.assert_not_called()

    @patch("cpc.services.price.mexc_market")
    def test_get_price_detail_03_api_error(self, mock_mexc, mock_console, test_user):
        mock_console.return_value = MagicMock()
        console = mock_console.return_value

        mock_mexc.return_value.get_24hr_ticker.side_effect = Exception(
            "No response from mexc market API")

        symbols = test_user["favorite"]
        service = PRICE_SERVICE()
        with pytest.raises(Exception) as e:
            service.get_price_detail(symbols)

        assert "No response from mexc market API" in str(e.value)
        console.print.assert_not_called()
