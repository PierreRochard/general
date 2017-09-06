from general.database.session_scope import session_scope


def create_login_api_trigger():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth_api.login(email TEXT, password TEXT) CASCADE;
        """)
        session.execute("""
                CREATE OR REPLACE FUNCTION
                  auth_api.login(email TEXT, password TEXT)
                  RETURNS auth.JWT_TOKEN
                LANGUAGE plpgsql
                AS $$
                DECLARE
                  _role  NAME;
                  result auth.JWT_TOKEN;
                BEGIN
                  SELECT auth.authenticate_user_email(email, password)
                  INTO _role;
                  IF _role IS NULL
                  THEN
                    RAISE invalid_password
                    USING MESSAGE = 'Invalid email or password';
                  END IF;
            
                  SELECT auth.jwt_sign(row_to_json(r), current_setting('app.jwt_secret')) AS token
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
                GRANT EXECUTE ON FUNCTION auth_api.login(TEXT, TEXT) TO anon;
                ''')


if __name__ == '__main__':
    create_login_api_trigger()
