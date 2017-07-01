import os

from models.util import session_scope

from postgrest_boilerplate.models.auth import Users


def insert_user(user_data):
    new_user = Users(**user_data)
    with session_scope() as session:
        session.add(new_user)


def insert_admin():
    user = {
        'email': os.environ['REST_EMAIL'],
        'password': os.environ['REST_PASSWORD'],
        'role': os.environ['REST_USER'],
    }
    insert_user(user)

if __name__ == '__main__':
    insert_admin()
