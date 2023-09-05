import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config.params import *

path = os.getcwd()
if DB_TYPE == 1:
    os_type = os.name
    if os_type == 'nt':
        DATABASE_URL = "sqlite:///" + path + '\\' + DB_SQLITE_NAME
    else:
        DATABASE_URL = "sqlite:///" + path + '/' + DB_SQLITE_NAME
elif DB_TYPE == 2:
    DATABASE_URL = "postgresql+psycopg2:://"\
                              + DB_USERNAME +\
                              ":" + DB_PASSWORD +\
                              "@" + DB_HOST +\
                              ':' + DB_PORT +\
                              "/" + DB_NAME
elif DB_TYPE == 3:
    DATABASE_URL = "mysql+mysqlconnector://" \
                              + DB_USERNAME +\
                              ":" + DB_PASSWORD +\
                              "@" + DB_HOST +\
                              "[:" + DB_PORT +\
                              "]/" + DB_NAME

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()