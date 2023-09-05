import os
DB_TYPE = 1 if os.getenv('DB_TYPE') is None else os.getenv('DB_TYPE')  # 1:sqlite, 2:postgres
DB_SQLITE_NAME = 'weat.db' if os.getenv('DB_SQLITE_NAME') is None else os.getenv('DB_SQLITE_NAME')
DB_HOST = '' if os.getenv('DB_HOST') is None else os.getenv('DB_HOST')
DB_USERNAME = '' if os.getenv('DB_USERNAME') is None else os.getenv('DB_USERNAME')
DB_PASSWORD = '' if os.getenv('DB_PASSWORD') is None else os.getenv('DB_PASSWORD')
DB_PORT = '' if os.getenv('DB_PORT') is None else os.getenv('DB_PORT')
DB_NAME = 'Some name' if os.getenv('DB_NAME') is None else os.getenv('DB_NAME')
TOKEN = {
    'SECRET_KEY': "" if os.getenv('TOKEN_SECRET_KEY') is None else os.getenv('TOKEN_SECRET_KEY'),
    'ALGORITHM': "" if os.getenv('TOKEN_ALGORITHM') is None else os.getenv('TOKEN_ALGORITHM'),
    'ACCESS_TOKEN_EXPIRE_MINUTES': 180
}
