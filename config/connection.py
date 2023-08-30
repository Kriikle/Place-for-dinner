import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config.params import *

path = os.getcwd()
if DB_TYPE == 1:
    os_type = os.name
    if os_type == 'nt':
        SQLALCHEMY_DATABASE_URL = "sqlite:///" + path + '\\' + DB_SQLITE_NAME
    else:
        SQLALCHEMY_DATABASE_URL = "sqlite:///" + path + '/' + DB_SQLITE_NAME
elif DB_TYPE == 2:
    SQLALCHEMY_DATABASE_URL = "postgresql://"\
                              + DB_USERNAME +\
                              ":" + DB_PASSWORD +\
                              "@" + DB_HOST +\
                              ':' + DB_PORT +\
                              "/" + DB_NAME
elif DB_TYPE == 3:
    SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://" \
                              + DB_USERNAME +\
                              ":" + DB_PASSWORD +\
                              "@" + DB_HOST +\
                              "[:" + DB_PORT +\
                              "]/" + DB_NAME

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()