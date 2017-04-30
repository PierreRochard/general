def install_user_table_functions(session):
    session.execute("GRANT SELECT ON TABLE auth.users TO anon;")

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

    DROP TRIGGER IF EXISTS ensure_user_role_exists
    ON auth.users;
    CREATE CONSTRAINT TRIGGER ensure_user_role_exists
    AFTER INSERT OR UPDATE ON auth.users
    FOR EACH ROW
    EXECUTE PROCEDURE auth.check_if_role_exists();
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
        new.password = crypt(new.password, gen_salt('bf', 8));
      END IF;
      RETURN new;
    END
    $$;

    DROP TRIGGER IF EXISTS encrypt_password
    ON auth.users;
    CREATE TRIGGER encrypt_password
    BEFORE INSERT OR UPDATE ON auth.users
    FOR EACH ROW
    EXECUTE PROCEDURE auth.encrypt_password();
    """)
