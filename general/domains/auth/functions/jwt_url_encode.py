from general.database.util import session_scope


def create_jwt_url_encode_function():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS  auth.jwt_url_encode(data BYTEA);
        """)

        session.execute("""
            CREATE OR REPLACE FUNCTION auth.jwt_url_encode(data BYTEA)
              RETURNS TEXT
            LANGUAGE SQL
            AS $$
            SELECT translate(encode(data, 'base64'), E'+/=\n', '-_');
            $$;
                """)
