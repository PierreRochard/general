
try:
    session.execute("""
            CREATE TYPE auth.jwt_token AS (
              token TEXT
            );
            """)
except ProgrammingError:
    session.rollback()
