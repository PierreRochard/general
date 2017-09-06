from general.database.session_scope import session_scope


def create_encrypt_password_function():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth.encrypt_password(_email TEXT, _password TEXT) CASCADE;
        """)

        session.execute("""
                CREATE OR REPLACE FUNCTION
                  auth.encrypt_password()
                  RETURNS TRIGGER
                LANGUAGE plpgsql
                AS $$
                BEGIN
                  IF tg_op = 'INSERT' OR new.password <> old.password
                  THEN
                    new.password = auth.crypt(new.password, auth.gen_salt('bf', 8));
                  END IF;
                  RETURN new;
                END
                $$;
            
                """)
