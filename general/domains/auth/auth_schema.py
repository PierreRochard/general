from general.database.schema import Schema
from general.database.session_scope import session_scope, Base

from general.domains.auth.functions import (
    create_authenticate_user_email_function,
    create_check_if_role_exists_function,
    create_encrypt_password_function,
    create_jwt_algorithm_sign_function,
    create_jwt_sign_function,
    create_jwt_url_encode_function
)
from general.domains.auth.models.users import Users


class AuthSchema(Schema):

    def __init__(self):
        super(AuthSchema, self).__init__(name='auth')

    def create_extensions(self):
        self.create_extension('pgcrypto')

    @staticmethod
    def create_types():
        with session_scope(raise_programming_error=False) as session:
            session.execute("""
                CREATE TYPE auth.jwt_token AS (
                  token TEXT
                );
                """)

    @staticmethod
    def create_tables():
        with session_scope() as session:
            Base.metadata.create_all(session.connection())

    @staticmethod
    def create_table_triggers():
        Users.create_triggers_on_users()
        Users.create_constraint_triggers_on_users()

    @staticmethod
    def create_functions():
        create_authenticate_user_email_function()
        create_check_if_role_exists_function()
        create_encrypt_password_function()

        create_jwt_url_encode_function()
        create_jwt_algorithm_sign_function()
        create_jwt_sign_function()

    def grant_auth_privileges(self):
        with session_scope(raise_programming_error=True) as session:
            privileges = {
                'ALL TABLES IN SCHEMA': {
                    'auth': {
                        'SELECT, UPDATE, INSERT': [u.role for u in
                                                   session.query(Users).all()]
                    }
                },
                'SCHEMA': {
                    'auth': {
                        'USAGE': [u.role for u in session.query(Users).all()]
                    }
                },
                'TABLE': {
                    'users': {
                        'SELECT': ['anon']
                    }
                }
            }
        self.grant_privileges(self.name, privileges)

    def setup(self):
        self.create_schema()
        self.create_extensions()
        self.create_types()
        self.create_tables()
        self.create_table_triggers()
        self.create_functions()
        self.grant_auth_privileges()
