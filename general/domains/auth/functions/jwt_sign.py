from general.database.util import session_scope


def create_encrypt_password_function():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth.sign(payload   JSON, secret TEXT,
                                              algorithm TEXT DEFAULT 'HS256' :: TEXT) CASCADE;
        """)

        session.execute("""
        CREATE OR REPLACE FUNCTION auth.sign(payload   JSON, secret TEXT,
                                  algorithm TEXT DEFAULT 'HS256' :: TEXT)
          RETURNS TEXT
        LANGUAGE SQL
        AS $$
        WITH
            header AS (
              SELECT auth.url_encode(
                         convert_to('{"alg":"' || algorithm || '","typ":"JWT"}',
                                    'utf8')) AS data
          ),
            payload AS (
              SELECT auth.url_encode(convert_to(payload :: TEXT, 'utf8')) AS data
          ),
            signables AS (
              SELECT header.data || '.' || payload.data AS data
              FROM header, payload
          )
        SELECT signables.data || '.' ||
               auth.algorithm_sign(signables.data, secret, algorithm)
        FROM signables;
        $$;
                """)
