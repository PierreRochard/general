import os

from models.auth import Users
from models.util import get_session

from scripts.insert_FormSettings import insert_form_settings
from scripts.insert_Submenus import insert_submenus
from scripts.insert_TableSettings import insert_table_settings


def insert_user(user_data):
    session = get_session()
    new_user = Users(**user_data)
    session.add(new_user)
    session.commit()

    insert_submenus(new_user['role'])
    insert_form_settings(new_user['role'])
    insert_table_settings(new_user['role'])


def insert_admin():
    user = {
        'email': os.environ['REST_EMAIL'],
        'password': os.environ['REST_PASSWORD'],
        'role': os.environ['REST_USER'],
    }
    insert_user(user)

if __name__ == '__main__':
    insert_admin()
