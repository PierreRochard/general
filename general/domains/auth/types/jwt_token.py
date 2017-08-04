from general.database.util import session_scope


def create_type_auth_jwt_token():
    with session_scope(raise_programming_error=False) as session:
        session.execute("""
            CREATE TYPE auth.jwt_token AS (
              token TEXT
            );
            """)
