from pprint import pprint
import unittest
import uuid

import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker

from models.admin import Submenus, TableSettings

from scripts import get_pg_url

api_path = 'https://api.rochard.org'
test_user_email = 'testing@localhost'
test_user_password = str(uuid.uuid4()).replace('-', '')


class TestRestAuth(unittest.TestCase):
    session = None

    def setUp(self):
        engine = create_engine(get_pg_url(), echo=True)
        self.session = scoped_session(sessionmaker(bind=engine, autocommit=False))()

    def test_unauthenticated(self):
        response = requests.get(api_path + '/')
        pprint(response)

        new_submenu = Submenus()
        new_submenu.submenu_name = 'Test'
        new_submenu.user = 'anon'
        try:
            self.session.add(new_submenu)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            new_submenu = (self.session.query(Submenus)
                           .filter(Submenus.submenu_name == 'Test')
                           .filter(Submenus.user == 'anon').one())

        new_table_setting = TableSettings()
        new_table_setting.table_name = 'messages'
        new_table_setting.user = 'anon'
        new_table_setting.submenu_id = str(new_submenu.id)
        try:
            self.session.add(new_table_setting)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

        new_table_setting = TableSettings()
        new_table_setting.table_name = 'column_settings'
        new_table_setting.user = 'anon'
        new_table_setting.submenu_id = str(new_submenu.id)
        try:
            self.session.add(new_table_setting)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

        params = dict(select="label,items{label, icon, routerLink}")
        response = requests.get(api_path + '/submenus', params=params).json()
        pprint(response)

    # def test_invalid_login(self):
    #     data = dict(email='wrong@localhost', password='wrongpassword')
    #     response = requests.post(api_path + '/rpc/login', data=data).json()
    #     assert response['code'] == '28P01'
    #     assert response['message'] == 'Invalid email or password'

    # def test_valid_login(self):
    #     data = dict(email=testing_email, password=testing_password)
    #     response = requests.post(api_path + '/rpc/login', data=data).json()
    #     pprint(response)
    #     token = response[0]['token']
    #     pprint(token)
    #     headers = {'Authorization': 'Bearer ' + token}
    #     response = requests.get(api_path + '/', headers=headers).json()
    #     pprint(response)


if __name__ == '__main__':
    unittest.main()
