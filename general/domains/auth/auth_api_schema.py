from general.database.schema import Schema
from general.database.util import session_scope
from general.domains.auth.models import Users

from general.domains.auth.api_functions import (
    create_login_api_trigger,
    create_logout_api_trigger
)


class AuthApiSchema(Schema):

    def __init__(self):
        super(AuthApiSchema, self).__init__(name='auth_api')

    @staticmethod
    def create_functions():
        create_login_api_trigger()
        create_logout_api_trigger()

    def grant_auth_privileges(self):
        with session_scope() as session:
            privileges = {
                'SCHEMA': {
                    'auth_api': {
                        'USAGE': [u.role for u in session.query(Users).all()]
                    }
                },
                'FUNCTION': {
                    'auth_api.login(TEXT, TEXT)': {
                        'EXECUTE': ['anon']
                    },
                    'auth_api.logout()': {
                        'EXECUTE': [u.role for u in session.query(Users).all()]
                    },
                },
            }
        self.grant_privileges(self.name, privileges)

if __name__ == '__main__':
    auth_api_schema = AuthApiSchema()
    auth_api_schema.create_schema()
    auth_api_schema.create_functions()
    auth_api_schema.grant_auth_privileges()
