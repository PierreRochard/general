from general.database.util import session_scope


def create_login_api_trigger(schema_name):
    with session_scope() as session:
        session.execute(f"""
            DROP FUNCTION IF EXISTS 
                {schema_name}.login(email TEXT, password TEXT) CASCADE;
        """)
        session.execute(f"""
                CREATE OR REPLACE FUNCTION
                  {schema_name}.login(email TEXT, password TEXT)
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
