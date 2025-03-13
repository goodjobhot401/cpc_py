import traceback
from cpc.services.favorite import FAVORITE_SERVICE


class FAVORITE:
    def add_favorite(favorite_list):
        try:
            user = FAVORITE_SERVICE()
            return user.add_favorite(favorite_list)

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def remove_favorite(favorite_list):
        try:
            user = FAVORITE_SERVICE()
            return user.remove_favorite(favorite_list)

        except Exception as e:
            print(f"Exception error: {e}")
            return
