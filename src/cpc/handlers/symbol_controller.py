import traceback
from cpc.services.symbol import SYMBOL_SERVICE


class SYMBOL:
    def filter_symbols(query=None):
        try:
            symbols = SYMBOL_SERVICE()
            symbols.filter_symbols(query)
            return

        except Exception as e:
            print(e)
            return
