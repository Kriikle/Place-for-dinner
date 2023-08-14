from fastapi import FastAPI
from sqlalchemy import MetaData
from v2.api import api_router


app = FastAPI()
app.include_router(api_router)
