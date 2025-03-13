import traceback
from cpc.services.price import PRICE_SERVICE


class PRICE:
    def get_price_detail(symbols):
        try:
            PRICE = PRICE_SERVICE()
            PRICE.get_price_detail(symbols)
            return

        except Exception as e:
            print(e)
            return
