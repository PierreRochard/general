from general.database.session_scope import session_scope


def create_check_if_role_exists_function():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS auth.check_if_role_exists() CASCADE;
        """)
        session.execute("""
                CREATE OR REPLACE FUNCTION
                  auth.check_if_role_exists()
                  RETURNS TRIGGER
                LANGUAGE plpgsql
                AS $$
                BEGIN
                  IF NOT exists(SELECT 1
                                FROM pg_roles
                                WHERE pg_roles.rolname = NEW.role)
                  THEN
                    RAISE foreign_key_violation
                    USING MESSAGE = 'Unknown database role: ' || NEW.role;
                    RETURN NULL;
                  END IF;
                  RETURN NEW;
                END
                $$;
          
                """)
