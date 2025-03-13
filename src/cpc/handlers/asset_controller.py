import traceback
from cpc.services.asset import ASSET_SERVICE


class ASSET:
    def add_asset(asset_list):
        try:
            user = ASSET_SERVICE()
            return user.add_asset(asset_list)

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def update_asset(asset_list):
        try:
            user = ASSET_SERVICE()
            return user.update_asset(asset_list)

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def remove_asset(asset_list):
        try:
            user = ASSET_SERVICE()
            return user.remove_asset(asset_list)

        except Exception as e:
            print(f"Exception error: {e}")
            return
