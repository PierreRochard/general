from general.database.util import session_scope


def create_logout_api_trigger(schema_name):
    with session_scope() as session:
        session.execute(f"""
                    CREATE OR REPLACE FUNCTION
                      {schema_name}.logout()
                      RETURNS VOID
                    LANGUAGE plpgsql
                    AS $$
                        BEGIN
                        END;
                    $$;
                """)
