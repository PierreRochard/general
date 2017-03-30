from models.auth import Users
from models.util import get_session


def insert_user(database, user, user_data):
    session = get_session(database, user)
    new_user = Users(**user_data)
    session.add(new_user)
    session.commit()
