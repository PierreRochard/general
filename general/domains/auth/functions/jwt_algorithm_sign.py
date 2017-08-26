from general.database.util import session_scope


def create_jwt_algorithm_sign_function():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth.jwt_algorithm_sign(signables TEXT, 
                                                        secret    TEXT,
                                                        algorithm TEXT);
        """)

        session.execute("""
    CREATE OR REPLACE FUNCTION auth.jwt_algorithm_sign(signables TEXT, secret TEXT,
                                                   algorithm TEXT)
      RETURNS TEXT
    LANGUAGE SQL
    AS $$
    WITH
        alg AS (
          SELECT CASE
                 WHEN algorithm = 'HS256'
                   THEN 'sha256'
                 WHEN algorithm = 'HS384'
                   THEN 'sha384'
                 WHEN algorithm = 'HS512'
                   THEN 'sha512'
                 ELSE '' END AS id) -- hmac throws error
    SELECT auth.jwt_url_encode(auth.hmac(signables, secret, alg.id))
    FROM alg;
    $$;
                """)
