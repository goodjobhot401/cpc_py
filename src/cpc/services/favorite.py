from cpc.helpers.mexc import mexc_market
from cpc.middlewares.db_connect import db_connection
from cpc.repositories.user import USER_REPOSITORIES
from cpc.repositories.favorite import FAVORITE_REPOSITORIES


class FAVORITE_SERVICE():
    @db_connection
    def __init__(self, conn):
        self.user_repository = USER_REPOSITORIES(conn)
        self.favorite_repository = FAVORITE_REPOSITORIES(conn)

    def add_favorite(self, favorite_list):
        try:
            user = self.user_repository.get_user()

            if not user:
                print("No user has been targeted.")
                return

            user_id = user.get("id")
            user_favorite = user.get("favorite")

            error_logs = []
            symbol_list = []
            for favorite in favorite_list:
                symbol = favorite.upper()
                params = {
                    "symbol": symbol
                }
                market = mexc_market()
                price = market.get_price(params)

                if price and "code" in price:
                    error_logs.append(favorite)
                elif price:
                    if symbol not in user_favorite:
                        symbol_list.append(symbol)
                else:
                    raise Exception(
                        f"No response from mexc market API: {symbol}")

            if error_logs:
                verb = "are" if len(error_logs) > 1 else "is"
                print(
                    f"{error_logs} {verb} invalid. \nCheck out by 'cpc symbols' command\n")

            if symbol_list:
                self.favorite_repository.add_favorite(user_id, symbol_list)
                print(f"Favorite {symbol_list} add success")
            return
        except Exception as e:
            raise Exception(f"{e}")

    def remove_favorite(self, favorite_list):
        user = self.user_repository.get_user()

        if not user:
            print("No user has been targeted.")
            return

        user_id = user.get("id")
        user_favorite = user.get("favorite")

        error_logs = []
        symbol_list = []
        for favorite in favorite_list:
            if favorite.upper() in user_favorite:
                symbol_list.append(favorite.upper())
            else:
                error_logs.append(favorite)

        if error_logs:
            verb = "are" if len(error_logs) > 1 else "is"
            print(
                f"{error_logs} {verb} not in your favorite list. \nCheck out your favorite by 'cpc favorite' command\n")

        if symbol_list:
            self.favorite_repository.remove_favorite(user_id, symbol_list)
            print(f"{symbol_list} remove success")

        return
