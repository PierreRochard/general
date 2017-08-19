from general.database.schema import Schema
from general.database.util import session_scope

from .api_functions import create_login_api_trigger, create_logout_api_trigger


class AuthApiSchema(Schema):
    name = 'auth_api'

    @classmethod
    def create_functions(cls):
        create_login_api_trigger(cls.name)
        create_logout_api_trigger(cls.name)

    @classmethod
    def grant_function_privileges(cls):
        with session_scope() as session:
            session.execute(f'''
                GRANT EXECUTE 
                    ON FUNCTION {cls.name}.login(TEXT, TEXT) 
                    TO anon;
                ''')
