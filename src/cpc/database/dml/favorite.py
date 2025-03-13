class FAVORITE_SQL():
    def add_favorite_sql(self):
        return '''
            INSERT INTO Favorite (symbol, user_id) 
            VALUES (?, ?)
            '''

    def remove_favorite_sql(self):
        return '''
            DELETE FROM Favorite 
            WHERE symbol = ? AND user_id = ?
            '''
