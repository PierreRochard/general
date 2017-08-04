from general.database.util import session_scope


def create_authenticate_user_email_function():
    """
    Returns the user's role name if the provided email and password are good
    """
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth.authenticate_user_email(_email TEXT, _password TEXT) CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE FUNCTION
              auth.authenticate_user_email(_email TEXT, _password TEXT)
              RETURNS NAME
            LANGUAGE plpgsql
            AS $$
            BEGIN
              RETURN (
                SELECT role
                FROM auth.users
                WHERE users.email = _email
                  AND users.password = auth.crypt(_password, users.password)
              );
            END;
            $$;
        """)

if __name__ == '__main__':
    create_authenticate_user_email_function()
