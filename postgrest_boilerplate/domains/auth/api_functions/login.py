

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

