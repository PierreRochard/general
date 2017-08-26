from general.database.util import session_scope


def create_encrypt_password_function():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth.sign(payload   JSON, secret TEXT,
                                              algorithm TEXT DEFAULT 'HS256' :: TEXT) CASCADE;
        """)

        session.execute("""
            CREATE OR REPLACE FUNCTION auth.url_encode(data BYTEA)
              RETURNS TEXT
            LANGUAGE SQL
            AS $$
            SELECT translate(encode(data, 'base64'), E'+/=\n', '-_');
            $$;
                """)
