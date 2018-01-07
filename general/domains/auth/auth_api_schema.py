from general.database.schema import Schema
from general.database.session_scope import session_scope
from general.domains.auth.models import Users

from general.domains.auth.api_functions import (
    create_login_api_trigger,
    create_logout_api_trigger,
    create_token_api_trigger
)


class AuthApiSchema(Schema):

    def __init__(self):
        super(AuthApiSchema, self).__init__(name='auth_api')

    @staticmethod
    def create_functions():
        create_login_api_trigger()
        create_logout_api_trigger()
        create_token_api_trigger()

    def grant_auth_privileges(self):
        with session_scope() as session:
            privileges = {
                'SCHEMA': {
                    'auth_api': {
                        'USAGE': [u.role for u in session.query(Users).all()]
                    }
                },
                'FUNCTION': {
                    'login(TEXT, TEXT)': {
                        'EXECUTE': ['anon']
                    },
                    'logout()': {
                        'EXECUTE': [u.role for u in session.query(Users).all()]
                    },
                    'token()': {
                        'EXECUTE': ['anon']
                    },
                },
            }
        self.grant_privileges(self.name, privileges)

    def setup(self):
        self.create_schema()
        self.create_functions()
        self.grant_auth_privileges()
