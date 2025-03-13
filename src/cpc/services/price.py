from rich.table import Table
from rich.console import Console
from cpc.helpers.mexc import mexc_market
from concurrent.futures import ThreadPoolExecutor
from cpc.common.const import PRICE_DETAIL_ROW_MAP as mapping


class PRICE_SERVICE():
    def get_price_detail(self, symbols):
        if not symbols:
            return

        ticker_price = {}
        with ThreadPoolExecutor(max_workers=10) as executor:
            market = mexc_market()
            futures = {
                executor.submit(market.get_24hr_ticker, {"symbol": symbol.upper()}): symbol
                for symbol in symbols
            }

            for future in futures:
                symbol = futures[future]
                try:
                    result = future.result()
                except Exception:
                    raise Exception(f"No response from mexc market API")

                if "code" in result:
                    raise Exception(
                        f"'{symbol}' is invalid. \nCheck out by 'cpc symbols' command\n")

                ticker_price[symbol] = result

        # Setup table
        console = Console()
        table = Table(title="", header_style="bold magenta", show_lines=True)
        table.add_column("symbol", justify="left", style="cyan")

        for symbol in symbols:
            table.add_column(
                ticker_price[symbol]["symbol"], justify="left", style="bold")

        for title, (key, default_color) in mapping.items():
            row = [f"{title}"]
            for symbol in symbols:
                value = ticker_price[symbol][key]
                if key in ("priceChange", "priceChangePercent", "quoteVolume"):
                    color = "bold red" if value[0] == "-" else "bold green"
                    sign = "" if value[0] == "-" else "+"
                    emoji = "🥵" if color == "bold red" else "🚀"
                    value_as_float = round(float(value.replace(",", "")), 4)
                    if key == "priceChange":
                        formatted_value = f"[{color}]{sign}{value_as_float}[/{color}] {emoji}"
                    elif key == "priceChangePercent":
                        value_percent = round(value_as_float * 100, 3)
                        formatted_value = f"[{color}]{sign}{value_percent}%[/{color}] {emoji}"
                    else:
                        quote_volume = f"{value_as_float:,.2f}"
                        formatted_value = f"{quote_volume}"
                elif default_color:
                    formatted_value = f"[{default_color}]{value}[/{default_color}]"
                else:
                    value = round(float(value.replace(",", "")), 4)
                    formatted_value = f"{value:,.3f}"
                row.append(f"{formatted_value}")
            table.add_row(*row)
        console.print(table)
        return
