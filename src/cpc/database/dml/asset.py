class ASSET_SQL():
    def add_asset_sql(self):
        return '''
            INSERT INTO Asset (symbol, amount, user_id) 
            VALUES (?, ?, ?)
            '''

    def update_asset_sql(self):
        return '''
            UPDATE Asset SET amount = ? 
            WHERE symbol = ? AND user_id = ?
            '''

    def remove_asset_sql(self):
        return '''
            DELETE FROM Asset 
            WHERE symbol = ? AND user_id = ?
            '''
