from postgrest_boilerplate.database.util import session_scope


def create_logout_api_trigger():
    with session_scope() as session:
        session.execute("""
                CREATE OR REPLACE FUNCTION
                  api.logout()
                  RETURNS VOID
                LANGUAGE plpgsql
                AS $$
                BEGIN
                END;
                $$;
                """)


if __name__ == '__main__':
    create_logout_api_trigger()
