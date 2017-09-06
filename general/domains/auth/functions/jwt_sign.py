from general.database.session_scope import session_scope


def create_jwt_sign_function():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth.jwt_sign(payload   JSON, secret TEXT) CASCADE;
        """)

        session.execute("""
        CREATE OR REPLACE FUNCTION auth.jwt_sign(payload   JSON, secret TEXT)
          RETURNS TEXT
        LANGUAGE SQL
        AS $$
        WITH
            header AS (
              SELECT auth.jwt_url_encode(
                         convert_to('{"alg":"HS256","typ":"JWT"}',
                                    'utf8')) AS data
          ),
            payload AS (
              SELECT auth.jwt_url_encode(convert_to(payload :: TEXT, 'utf8')) AS data
          ),
            signables AS (
              SELECT header.data || '.' || payload.data AS data
              FROM header, payload
          )
        SELECT signables.data || '.' ||
               auth.jwt_algorithm_sign(signables.data, secret, 'HS256')
        FROM signables;
        $$;
                """)
