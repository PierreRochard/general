ALTER DATABASE rest SET "app.jwt_secret" TO '4S7lR9SnY8g3';
ALTER DATABASE rest SET "app.jwt_hours" TO 24;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pgjwt;

CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS api;

CREATE ROLE anon;
CREATE ROLE authenticator NOINHERIT;
GRANT anon TO authenticator;

GRANT USAGE ON SCHEMA api, auth TO anon;
GRANT EXECUTE ON FUNCTION api.login(TEXT, TEXT) TO anon;


CREATE TABLE
  auth.users (
  email    TEXT PRIMARY KEY CHECK ( email ~* '^.+@.+\..+$' ),
  password TEXT NOT NULL CHECK (length(password) < 512),
  role     NAME NOT NULL CHECK (length(role) < 512)
);

GRANT SELECT ON TABLE pg_authid, auth.users TO anon;

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

CREATE OR REPLACE FUNCTION
  auth.user_role(_email TEXT, _password TEXT)
  RETURNS NAME
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN (
    SELECT role
    FROM auth.users
    WHERE users.email = _email
          AND users.password = crypt(_password, users.password)
  );
END;
$$;

CREATE TYPE auth.jwt_token AS (
  token TEXT
);

CREATE OR REPLACE FUNCTION
  api.login(email TEXT, password TEXT)
  RETURNS auth.jwt_token
LANGUAGE plpgsql
AS $$
DECLARE
  _role  NAME;
  result auth.jwt_token;
BEGIN
  SELECT auth.user_role(email, password)
  INTO _role;
  IF _role IS NULL
  THEN
    RAISE invalid_password
    USING MESSAGE = 'Invalid email or password';
  END IF;

  SELECT sign(row_to_json(r), current_setting('app.jwt_secret')) AS token
  FROM (
         SELECT
           _role            AS role,
           email            AS email,
           extract(EPOCH FROM now()) :: INTEGER + current_setting('app.jwt_hours')::INTEGER * 60 * 60 AS exp
       ) r
  INTO result;
  RETURN result;
END;
$$;

CREATE TABLE api.messages (
  id        UUID PRIMARY KEY   DEFAULT gen_random_uuid(),
  time      TIMESTAMP   NOT NULL DEFAULT now(),
  from_user NAME      NOT NULL DEFAULT current_user,
  to_user   NAME      NOT NULL,
  subject   VARCHAR(64) NOT NULL,
  body      TEXT
);

CREATE POLICY message_policy
  ON api.messages
USING ((to_user = current_user) OR (from_user = current_user))
WITH CHECK (from_user = current_user)
