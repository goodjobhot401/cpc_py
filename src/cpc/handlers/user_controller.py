import traceback
from cpc.services.user import USER_SERVICE


class USER:
    def create_default_user():
        try:
            user = USER_SERVICE()
            return user.create_default_user()

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def get_users():
        try:
            user = USER_SERVICE()
            return user.get_users()

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def get_user(print_table=None):
        try:
            user = USER_SERVICE()
            return user.get_user(print_table)

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def switch_user(user_id=None):
        try:
            user = USER_SERVICE()
            return user.switch_user(user_id)

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def create_user(name):
        try:
            user = USER_SERVICE()
            if not name == ["-1"]:
                return user.create_user(name)
            else:
                return user.create_default_user()

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def update_user(user_id, name):
        try:
            user = USER_SERVICE()
            return user.update_user(user_id, name)

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def remove_user(user_id):
        try:
            user = USER_SERVICE()
            return user.remove_user(user_id)

        except Exception as e:
            print(f"Exception error: {e}")
            return

    def get_position_ratio(sort, reverse):
        try:
            user = USER_SERVICE()
            return user.get_position_ratio(sort, reverse)

        except Exception as e:
            print(f"Exception error: {e}")
            return
