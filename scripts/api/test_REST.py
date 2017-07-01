from pprint import pprint
import unittest
import uuid

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
        data = dict(label='Test')
        new_submenu = requests.post(api_path + '/submenus', data=data)
        print(new_submenu.json())

        test_submenu = requests.get(api_path + '/submenus').json()
        test_submenu = [s for s in test_submenu if s['label'] == 'Test'][0]

        data = dict(table_name='messages',
                    user='anon',
                    submenu_id=test_submenu['id'],
                    )
        new_table_setting = requests.post(api_path + '/table_settings',
                                          data=data)

        data = dict(table_name='column_settings',
                    user='anon',
                    submenu_id=test_submenu['id'],
                    )
        new_table_setting = requests.post(api_path + '/table_settings',
                                          data=data)

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
