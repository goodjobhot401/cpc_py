import os

# sqlite3
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(BASE_DIR, "database", "cpc.db")

# mexc api
MEXC_HOST = "https://api.mexc.com"