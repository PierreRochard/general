import os
from pprint import pprint
import unittest
import uuid

import requests
from sqlalchemy.engine.url import URL

host = 'localhost'
port = 5432
database_name = 'rest_auth_test'
admin_user = 'test_admin'
admin_password = os.environ.get('TEST_ADMIN_PASSWORD')
api_path = 'http://localhost:4545'
test_user_email = 'testing@localhost'
test_user_password = str(uuid.uuid4()).replace('-', '')

pg_uri = URL(drivername='postgresql+psycopg2',
             username=admin_user,
             password=admin_password,
             host=host,
             port=port,
             database=database_name)


class TestRestAuth(unittest.TestCase):
    def setUp(self):


    def test_unauthenticated(self):
        response = requests.get(api_path + '/').json()
        pprint(response)

    def test_invalid_login(self):
        data = dict(email='wrong@localhost', password='wrongpassword')
        response = requests.post(api_path + '/rpc/login', data=data).json()
        assert response['code'] == '28P01'
        assert response['message'] == 'Invalid email or password'

    def test_valid_login(self):
        data = dict(email=testing_email, password=testing_password)
        response = requests.post(api_path + '/rpc/login', data=data).json()
        pprint(response)
        token = response[0]['token']
        pprint(token)
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.get(api_path + '/', headers=headers).json()
        pprint(response)


if __name__ == '__main__':
    unittest.main()
