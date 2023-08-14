from core.models import restaurant, user
from config.connection import SessionLocal, engine

restaurant.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
