from general.database.session_scope import session_scope


def create_token_api_trigger():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth_api.token() CASCADE;
        """)
        session.execute("""
                CREATE OR REPLACE FUNCTION
                  auth_api.token()
                  RETURNS auth.JWT_TOKEN
                LANGUAGE plpgsql
                AS $$
                DECLARE
                  result auth.JWT_TOKEN;
                BEGIN

                  SELECT auth.jwt_sign(row_to_json(r), current_setting('app.jwt_ws_secret')) AS token
                  FROM (
                         SELECT
                           'anon' AS role,
                           'rw' AS mode,
                           extract(EPOCH FROM now()) :: INTEGER + current_setting('app.jwt_hours')::INTEGER * 60 * 60 AS exp
                       ) r
                  INTO result;
                  RETURN result;
                END;
                $$;
                """)
