import plotext as plt
from datetime import datetime
from cpc.helpers.mexc import mexc_market
from cpc.common.const import VALID_INTERVAL


class KLINE_SERVICE():
    def get_kline(self, symbol, interval, limit, test=False):
        if interval not in VALID_INTERVAL:
            print(
                f'{interval} is valid, --interval only accepts the following values: \n{VALID_INTERVAL}\n\n- m  → minute\n- h  → hour\n- d  → day\n- W  → week\n- M  → month\n')
            print("Please pay attention to the case sensitivity")
            return

        market = mexc_market()
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit
        }
        try:
            kline = market.get_kline(params)
        except Exception:
            raise Exception("No response from mexc market API")

        kline_data = [list(map(str, k_line)) for k_line in kline]
        self._plot_candlesticks(kline_data, symbol, interval, test)
        return

    def _plot_candlesticks(self, klines_data, symbol, interval, test):
        if not test:
            dates = []
            data = {
                "Open": [],
                "High": [],
                "Low": [],
                "Close": []
            }

            for candle in klines_data:
                dt = datetime.fromtimestamp(int(candle[0]) / 1000)
                date_str = dt.strftime('%d/%m/%Y %H:%M:%S')
                dates.append(date_str)

                data["Open"].append(float(candle[1]))
                data["High"].append(float(candle[2]))
                data["Low"].append(float(candle[3]))
                data["Close"].append(float(candle[4]))

            plt.date_form('d/m/Y H:M:S')
            plt.plot_size(100, 20)
            plt.candlestick(
                dates=dates,
                data=data,
                colors=["green", "red"],
                label=symbol.upper()
            )

            plt.title(f"{symbol.upper()} {interval} K-Line")
            plt.grid(True)
            plt.show()
