from cpc.services.kline import KLINE_SERVICE


class KLINE:
    def get_kline(symbol, interval, limit):
        try:
            KLINE = KLINE_SERVICE()
            KLINE.get_kline(symbol, interval, limit)
            return

        except Exception as e:
            print(e)
            return
