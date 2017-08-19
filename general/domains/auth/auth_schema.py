from general.database.schema import Schema
from general.database.util import session_scope

from .functions import (create_authenticate_user_email_function,
                        create_check_if_role_exists_function,
                        create_encrypt_password_function)
from .models.users import Users


class AuthSchema(Schema):
    name = 'auth'

    def __init__(self):
        super(AuthSchema, self).__init__()

    def create_extensions(self):
        extensions = ('pgcrypto', 'pgjwt')
        for extension in extensions:
            self.create_extension(self.name, extension)

    @staticmethod
    def create_functions():
        create_authenticate_user_email_function()
        create_check_if_role_exists_function()
        create_encrypt_password_function()

    @staticmethod
    def create_table_triggers():
        Users.create_triggers_on_users()
        Users.create_constraint_triggers_on_users()

    @staticmethod
    def create_types():
        with session_scope(raise_programming_error=False) as session:
            session.execute("""
                CREATE TYPE auth.jwt_token AS (
                  token TEXT
                );
                """)

    def grant_auth_privileges(self):
        privileges = {
            'TABLE': {
                'users': {
                    'SELECT': ['anon']
                }
            }
        }
        self.grant_privileges(self.name, privileges)
