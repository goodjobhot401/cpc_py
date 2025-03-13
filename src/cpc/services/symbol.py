import json
from rich.table import Table
from rich.console import Console
from cpc.helpers.mexc import mexc_market


class SYMBOL_SERVICE():
    def filter_symbols(self, query=None):
        try:
            symbols_data = mexc_market().get_defaultSymbols()
        except Exception:
            raise Exception("No response from mexc market API")

        symbols = symbols_data["data"]

        grouped_lists = {chr(i): [] for i in range(65, 91)}  # A-Z
        grouped_lists["0"] = []

        for symbol in symbols:
            first_char = symbol[0].upper()
            grouped_lists.setdefault(
                first_char if first_char in grouped_lists else "0", []).append(symbol)

        console = Console()
        table = Table(title="", header_style="bold magenta", show_lines=True)

        table.add_column(
            "Query String" if query else "Alphabetical Index", justify="full", style="cyan")
        table.add_column("Available Symbols", justify="full", style="bold")

        if query:
            query_upper = query.upper()
            query_list = grouped_lists[query_upper[0]]
            symbol_list = list(
                filter(lambda item: query_upper in item, query_list))
            sorted_list = sorted(symbol_list)

            table.add_row(query, json.dumps(sorted_list, indent=4))
            console.print(table)
            return

        for key in grouped_lists:
            table.add_row(key, json.dumps(
                sorted(grouped_lists[key]), indent=4))
        console.print(table)
        return
