import json
from rich.table import Table
# from term_piechart import Pie
from rich.console import Console
from cpc.helpers.mexc import mexc_market
from cpc.repositories.user import USER_REPOSITORIES
from cpc.middlewares.db_connect import db_connection
from concurrent.futures import ThreadPoolExecutor


class USER_SERVICE():
    @db_connection
    def __init__(self, conn):
        self.repository = USER_REPOSITORIES(conn)

    def create_default_user(self):
        self.repository.create_default_user()
        return

    def get_users(self):
        users = self.repository.get_users()

        if users:
            console = Console()
            table = Table(title="", header_style="bold magenta",
                          show_lines=True)
            table.add_column("ID", justify="full", style="bold cyan")
            table.add_column("Name", justify="full", style="bold yellow")
            table.add_column("Target", justify="full")

            for user in users:
                table.add_row(
                    str(user["id"]),
                    user["name"],
                    "[green]True[/green]" if user["target"] else "False"
                )
            console.print(table)
        return

    def get_user(self, print_table=False):
        user = self.repository.get_user()

        if user and not print_table:
            return user
        elif user:
            console = Console()
            table = Table(title="", header_style="bold magenta")
            table.add_column("ID", justify="full", style="bold cyan")
            table.add_column("Name", justify="full", style="bold yellow")
            table.add_column("Favorite", justify="full", style="bold")
            table.add_column("Asset", justify="full", style="bold")
            table.add_column("Target", justify="full", style="bold green")

            table.add_row(
                str(user["id"]),
                user["name"],
                json.dumps(user["favorite"], indent=4),
                json.dumps(user["asset"], indent=4),
                "True" if user["target"] else "False"
            )
            console.print(table)
            return None
        else:
            return None

    def switch_user(self, user_id=None):
        if user_id:
            try:
                user_id = int(user_id)
            except Exception:
                raise Exception(
                    f"Parameter 'user_id' have to be an integer. \nExample: 1\n")
        self.repository.switch_user(user_id)
        return

    def create_user(self, name):
        full_name = " ".join(name)
        self.repository.create_user(full_name)
        return

    def update_user(self, user_id, name):
        try:
            user_id = int(user_id)
        except Exception:
            raise Exception(
                f"Parameter format have to be 'user_id name'. \nExample: 1 Tom Yung\n")
        new_name = " ".join(name)
        self.repository.update_user(user_id, new_name)
        return

    def remove_user(self, user_id):
        try:
            user_id = int(user_id)
        except Exception:
            raise Exception(
                f"Parameter have to be an integer. \nExample: 1\n")
        self.repository.remove_user(user_id)
        return

    def get_position_ratio(self, sort="value", reverse="True", pie="False"):
        user = self.repository.get_user()
        postition_list = user.get("asset")

        reverse_flag = True if reverse.upper() == "TRUE" else False
        pie_flag = True if pie.upper() == "TRUE" else False

        ticker_price = {}
        ticker_price_list = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            market = mexc_market()
            futures = {
                executor.submit(market.get_price, {"symbol": postition["symbol"].upper()}): postition
                for postition in postition_list
            }
            for future in futures:
                try:
                    result = future.result()
                    ticker_price[result["symbol"].upper()] = result
                except Exception:
                    raise Exception(f"No response from mexc market API")

        total = 0
        for postition in postition_list:
            symbol = postition["symbol"]
            amount = postition["amount"]
            price = ticker_price[symbol.upper()]["price"]
            value = round(float(amount) * float(price), 2)

            data = {
                "symbol": symbol.upper(),
                "amount": amount,
                "price": float(price),
                "value": float(value),
            }
            ticker_price_list.append(data)
            total += value

        total = round(total, 2)
        for ticker_price in ticker_price_list:
            percentage = round(
                float(ticker_price["value"]) / float(total) * 100, 2)
            ticker_price["percentage"] = percentage

        # if pie_flag:
        #     sorted_ticker_price = sorted(
        #         ticker_price_list, key=lambda ticker: ticker["value"], reverse=True)
        #     return self.get_position_ratio_pie(sorted_ticker_price)

        sort_logic = ["symbol", "amount", "value"]
        if sort.lower() not in sort_logic:
            return "Parameter 'sort' must be 'symbol', 'amount' or 'value'."

        sorted_ticker_price = sorted(
            ticker_price_list, key=lambda ticker: ticker[sort.lower()], reverse=reverse_flag)

        console = Console()
        table = Table(
            title=f"[bold gold1]{user["name"]}[/bold gold1] total asset approx: [bold green]{total}[/bold green] usdt",
            header_style="bold magenta",
            show_lines=True)

        columns = ["Symbol", "Amount", "Latest Price",
                   "Market Value", "Percentage"]
        for column in columns:
            style = ""
            if column == "Symbol":
                style = " cyan"
            elif column == "Market Value":
                style = " green"
            elif column == "Percentage":
                style = "bold yellow"
            table.add_column(column, justify="left", style=style)

        for ticker_price in sorted_ticker_price:
            table.add_row(
                f'\n{str(ticker_price["symbol"])}\n',
                f'\n{str(ticker_price["amount"])}\n',
                f'\n{str(ticker_price["price"])}\n',
                f'\n{str(ticker_price["value"])}\n',
                f'\n{ticker_price["percentage"]}%\n'
            )
        console.print(table)
        return

    # def get_position_ratio_pie(self, postition_list):
    #     pie_data = []
    #     for ticker in postition_list:
    #         data = {}
    #         data["name"] = ticker["symbol"]
    #         data["value"] = ticker["value"]
    #         pie_data.append(data)

    #     pie = Pie(
    #         pie_data,
    #         radius=5,
    #         autocolor=False,
    #         autocolor_pastel_factor=0.5,
    #         legend={
    #             "line": 0,
    #             "format": "{label} {name:<8} {percent:>5.2f}% [{value} usdt]"
    #         },
    #     )
    #     print(f"\n{pie.render()}")
    #     return
