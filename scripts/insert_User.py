import os

from sqlalchemy.exc import IntegrityError

from models.auth import Users
from models.util import get_session


def insert_user(user_data):
    session = get_session()
    new_user = Users(**user_data)
    try:
        session.add(new_user)
        session.commit()
    except IntegrityError:
        session.rollback()


def insert_admin():
    user = {
        'email': os.environ['REST_EMAIL'],
        'password': os.environ['REST_PASSWORD'],
        'role': os.environ['REST_USER'],
    }
    insert_user(user)

if __name__ == '__main__':
    insert_admin()
