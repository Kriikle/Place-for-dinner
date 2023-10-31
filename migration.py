from core.models import restaurant, user, dinner
from config.connection import SessionLocal, engine, get_db
from core.models.user import User
from core.schemas.user import UserCreateAdmin
from v1.functions.auth import get_password_hash
from v1.functions.crud import create_


db = get_db().__next__()
user.Base.metadata.create_all(bind=engine)
restaurant.Base.metadata.create_all(bind=engine)
dinner.Base.metadata.create_all(bind=engine)
new_row = UserCreateAdmin(
    login='Admin',
    password='',
    email='log@aq.ru',
    firstname=None,
    lastname=None,
    patronymic=None,
    is_admin=True,
)
new_row.password = get_password_hash(new_row.password)
create_(User, new_row, db)
