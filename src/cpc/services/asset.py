from cpc.helpers.mexc import mexc_market
from cpc.middlewares.db_connect import db_connection
from cpc.repositories.user import USER_REPOSITORIES
from cpc.repositories.asset import ASSET_REPOSITORIES


class ASSET_SERVICE():
    @db_connection
    def __init__(self, conn):
        self.user_repository = USER_REPOSITORIES(conn)
        self.asset_repository = ASSET_REPOSITORIES(conn)

    def add_asset(self, asset_list):
        try:
            user = self.user_repository.get_user()

            if not user:
                print("No user has been targeted.")
                return

            if len(asset_list) % 2 != 0:
                print(
                    f"Parameter format have to be 'symbol amount'. \nExample: btcusdt 0.5 ethusdt 2.5\n")
                return
            user_id = user.get("id")
            user_asset_symbol = [asset["symbol"]
                                 for asset in user.get("asset")]

            error_logs = []
            symbol_list = []
            for i in range(0, len(asset_list), 2):
                symbol = asset_list[i].upper()
                amount = asset_list[i+1]

                try:
                    _ = float(amount)
                except ValueError:
                    print(
                        f"Parameter format have to be 'symbol amount'. \nExample: btcusdt 0.5 ethusdt 2.5\n")
                    return

                params = {
                    "symbol": symbol
                }
                market = mexc_market()
                price = market.get_price(params)

                if price and "code" in price:
                    error_logs.append(symbol)
                elif price:
                    if symbol not in user_asset_symbol:
                        symbol_list.append({
                            "symbol": symbol,
                            "amount": float(amount)
                        })
                else:
                    raise Exception(
                        f"No response from mexc market API: {symbol}")

            if error_logs:
                verb = "are" if len(error_logs) > 1 else "is"
                print(
                    f"{error_logs} {verb} invalid. \nCheck out by 'cpc symbols' command\n")

            if symbol_list:
                self.asset_repository.add_asset(user_id, symbol_list)
                print(f"Asset {symbol_list} add success")
            return
        except Exception as e:
            raise Exception(f"{e}")

    def update_asset(self, asset_list):
        user = self.user_repository.get_user()

        if not user:
            print("No user has been targeted.")
            return

        if len(asset_list) % 2 != 0:
            print(
                f"Parameter format have to be 'symbol amount'. \nExample: btcusdt 0.5 ethusdt 2.5\n")
            return

        user_id = user.get("id")
        user_asset_symbol = [asset["symbol"] for asset in user.get("asset")]

        error_logs = []
        symbol_list = []
        for i in range(0, len(asset_list), 2):
            symbol = asset_list[i].upper()
            amount = asset_list[i+1]

            try:
                _ = float(amount)
            except ValueError:
                print(
                    f"Parameter format have to be 'symbol amount'. \nExample: btcusdt 0.5 ethusdt 2.5\n")
                return

            if symbol not in user_asset_symbol:
                error_logs.append(asset_list[i])
            else:
                symbol_list.append({
                    "symbol": symbol,
                    "amount": float(amount)
                })

        if error_logs:
            verb = "are" if len(error_logs) > 1 else "is"
            print(
                f"{error_logs} {verb} not in your asset list. \nCheck out your asset by 'cpc asset' command\n")

        if symbol_list:
            self.asset_repository.update_asset(user_id, symbol_list)
            print(f"Asset {symbol_list} update success")
        return

    def remove_asset(self, asset_list):
        user = self.user_repository.get_user()

        if not user:
            print("No user has been targeted.")
            return

        user_id = user.get("id")
        user_asset_symbol = [asset["symbol"] for asset in user.get("asset")]

        error_logs = []
        symbol_list = []
        for asset in asset_list:
            if asset.upper() in user_asset_symbol:
                symbol_list.append(asset.upper())
            else:
                error_logs.append(asset)

        if error_logs:
            verb = "are" if len(error_logs) > 1 else "is"
            print(
                f"{error_logs} {verb} not in your asset list. \nCheck out your favorite by 'cpc favorite' command\n")

        if symbol_list:
            self.asset_repository.remove_asset(user_id, symbol_list)
            print(f"{symbol_list} remove success")

        return
