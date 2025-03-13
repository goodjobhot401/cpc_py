class USER_SQL():
    def create_user(self):
        return '''
            INSERT INTO user (name, target) 
            VALUES (?, ?)
            '''

    def get_users(self):
        return '''
            SELECT * FROM user
            '''

    def get_user(self):
        return '''
            SELECT * FROM user 
            WHERE target = 1
            '''

    def get_favorite_sql(self):
        return '''
            SELECT symbol FROM favorite 
            WHERE user_id = ?
            '''

    def get_asset_sql(self):
        return '''
            SELECT symbol, amount FROM asset 
            WHERE user_id = ?
            '''

    def is_taget_sql(self):
        return '''
            SELECT * FROM user 
            WHERE target = 1
            '''

    def remove_all_target(self):
        return '''
            UPDATE user SET target = 0 
            WHERE target = 1
            '''

    def auto_choose_user(self):
        return '''
            UPDATE user SET target = 1 
            WHERE id = (SELECT id FROM user ORDER BY id ASC LIMIT 1)
            '''

    def switch_target_user(self):
        return '''
            UPDATE user SET target = 1 WHERE id = ?
            '''

    def update_user(self, fields):
        return f'''
            UPDATE user SET {", ".join(fields)} WHERE id = ?
            '''

    def remove_user_sql(self):
        return '''
            DELETE FROM user 
            WHERE id = ?
            '''

    def remove_favorite_sql(self):
        return '''
            DELETE FROM favorite 
            WHERE user_id = ?
            '''

    def remove_asset_sql(self):
        return '''
            DELETE FROM asset 
            WHERE user_id = ?
            '''
