from sqlalchemy.orm import Session

from core.models import restaurant, user, dinner, limit
from config.connection import SessionLocal, engine, get_db
from core.models.limit import Limit
from core.models.user import User


dict_first_admin = {
    'login': "Admin",
    'password': "123",
    'email': "log@aq.ru",
    'firstname': None,
    'lastname': None,
    'patronymic': None,
    'is_admin': True,
}
user.Base.metadata.create_all(bind=engine)
restaurant.Base.metadata.create_all(bind=engine)
dinner.Base.metadata.create_all(bind=engine)
limit.Base.metadata.create_all(bind=engine)

with Session(engine) as session:
    session.add(Limit(**dict({'name': "Registration(no accept mail)", 'limit_cafes': 10, 'limit_hist_visit': 30})))
    session.add(Limit(**dict({'name': "Registration (with mail)", 'limit_cafes': 30, 'limit_hist_visit': 50})))
    session.add(Limit(**dict({'name': "Prize min", 'limit_cafes': 50, 'limit_hist_visit': 100})))
    session.add(Limit(**dict({'name': "Prize medium", 'limit_cafes': 100, 'limit_hist_visit': 200})))
    session.add(Limit(**dict({'name': "Prize big", 'limit_cafes': 300, 'limit_hist_visit': 500})))
    session.commit()
    session.add(User(**dict(dict_first_admin)))
    session.commit()
