import os
DB_TYPE = os.getenv('DB_TYPE',1)  # 1:sqlite, 2:postgres
DB_SQLITE_NAME = os.getenv('DB_TYPE', 'weat.db')
DB_HOST = os.getenv('DB_HOST', '')
DB_USERNAME = os.getenv('DB_USERNAME', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_PORT = os.getenv('DB_PORT', '')
DB_NAME = os.getenv('DB_NAME', '')
TOKEN = {
    'SECRET_KEY': os.getenv('TOKEN_SECRET_KEY', ''),
    'ALGORITHM': os.getenv('TOKEN_ALGORITHM', 'HS256'),
    'ACCESS_TOKEN_EXPIRE_MINUTES': 30
}
