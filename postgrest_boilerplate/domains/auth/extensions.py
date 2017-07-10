# Todo: there are namespacing problems with extensions
# Fix this in ansible, not in here
# Dirty hack is to add schemas to the search path in postgres config
from postgrest_boilerplate.database.util import session_scope


def create_auth_extensions():
    with session_scope(raise_programming_error=True) as session:
        session.execute("""
        DROP EXTENSION IF EXISTS pgcrypto CASCADE; 
        CREATE EXTENSION pgcrypto SCHEMA auth;
        """)
    with session_scope(raise_programming_error=True) as session:
        session.execute("""
        DROP EXTENSION IF EXISTS pgjwt CASCADE; 
        CREATE EXTENSION pgjwt SCHEMA auth;
        """)
if __name__ == '__main__':
    create_auth_extensions()
