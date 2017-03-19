def install_login_function(session):
    session.execute( """
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
              AND users.password = crypt(_password, users.password)
      );
    END;
    $$;
    """)

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

      SELECT sign(row_to_json(r), current_setting('app.jwt_secret')) AS token
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
        api.websocket_login(channel TEXT)
        RETURNS auth.jwt_token
    LANGUAGE plpgsql
    AS $$
    DECLARE
    """)
