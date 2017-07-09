
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
session.execute('''
        GRANT EXECUTE ON FUNCTION api.logout() TO anon;
        ''')
