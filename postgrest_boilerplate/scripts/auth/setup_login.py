from sqlalchemy.exc import ProgrammingError

from postgrest_boilerplate.models.util import session_scope


def install_login_function():
    with session_scope() as session:
        # Todo: there are namespacing problems with extensions
        # Fix this in ansible, not in here
        # Dirty hack is to add schemas to the search path in postgres config
        # session.execute("""
        # CREATE EXTENSION pgcrypto SCHEMA auth;
        # CREATE EXTENSION pgjwt SCHEMA auth;
        # """)
        session.execute("""
        CREATE OR REPLACE FUNCTION
          auth.user_role(_email TEXT, _password TEXT)
          RETURNS NAME
        LANGUAGE plpgsql
        AS $$
        BEGIN
          RETURN (
            SELECT role
            FROM auth.users
            WHERE users.email = _email
                  AND users.password = auth.crypt(_password, users.password)
          );
        END;
        $$;
        """)

        try:
            session.execute("""
            CREATE TYPE auth.jwt_token AS (
              token TEXT
            );
            """)
        except ProgrammingError:
            session.rollback()

        session.execute("""
        CREATE OR REPLACE FUNCTION
          api.login(email TEXT, password TEXT)
          RETURNS auth.jwt_token
        LANGUAGE plpgsql
        AS $$
        DECLARE
          _role  NAME;
          result auth.jwt_token;
        BEGIN
          SELECT auth.user_role(email, password)
          INTO _role;
          IF _role IS NULL
          THEN
            RAISE invalid_password
            USING MESSAGE = 'Invalid email or password';
          END IF;
    
          SELECT auth.sign(row_to_json(r), current_setting('app.jwt_secret')) AS token
          FROM (
                 SELECT
                   _role            AS role,
                   email            AS email,
                   extract(EPOCH FROM now()) :: INTEGER + current_setting('app.jwt_hours')::INTEGER * 60 * 60 AS exp
               ) r
          INTO result;
          RETURN result;
        END;
        $$;
        """)
        session.execute('''
        GRANT EXECUTE ON FUNCTION api.login(TEXT, TEXT) TO anon;
        ''')

        session.execute("""
        CREATE OR REPLACE FUNCTION
          api.logout()
          RETURNS VOID
        LANGUAGE plpgsql
        AS $$
        BEGIN
        END;
        $$;
        """)
        session.execute('''
        GRANT EXECUTE ON FUNCTION api.logout() TO anon;
        ''')


        # session.execute("""
        # CREATE OR REPLACE FUNCTION
        #     api.websocket_login(channel TEXT)
        #     RETURNS auth.jwt_token
        # LANGUAGE plpgsql
        # AS $$
        # DECLARE
        # """)
