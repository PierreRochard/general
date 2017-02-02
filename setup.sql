ALTER DATABASE rest SET "app.jwt_secret" TO 'SECRET';
ALTER DATABASE rest SET "app.jwt_hours" TO 24;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pgjwt;

create schema if not exists auth;
create schema if not exists api;

create table
auth.users (
  email    text primary key check ( email ~* '^.+@.+\..+$' ),
  password text not null check (length(password) < 512),
  role     name not null check (length(role) < 512)
);

create or replace function
auth.check_if_role_exists() returns trigger
  language plpgsql
  as $$
begin
  if not exists (select 1 from pg_roles where pg_roles.rolname = NEW.role) then
    raise foreign_key_violation using message = 'Unknown database role: ' || NEW.role;
    return null;
  end if;
  return NEW;
end
$$;

drop trigger if exists ensure_user_role_exists on auth.users;
create constraint trigger ensure_user_role_exists
  after insert or update on auth.users
  for each row
  execute procedure auth.check_if_role_exists();


create or replace function
auth.encrypt_password() returns trigger
  language plpgsql
  as $$
begin
  if tg_op = 'INSERT' or new.password <> old.password then
    new.password = crypt(new.password, gen_salt('bf', 8));
  end if;
  return new;
end
$$;

drop trigger if exists encrypt_password on auth.users;
create trigger encrypt_password
  before insert or update on auth.users
  for each row
  execute procedure auth.encrypt_password();

create or replace function
auth.user_role(email text, password text) returns name
language plpgsql
as $$
  begin
    return (
      select role from auth.users
       where users.email = email
         and users.password = crypt(password, users.password)
    );
  end;
$$;

CREATE TYPE auth.jwt_token AS (
  token text
);

create or replace function
api.login(email text, pass text) returns auth.jwt_token
  language plpgsql
  as $$
declare
  _role name;
  result auth.jwt_token;
begin
  select auth.user_role(email, pass) into _role;
  if _role is null then
    raise invalid_password using message = 'Invalid email or password';
  end if;

  select sign(row_to_json(r), current_setting('app.jwt_secret')) as token
    from (
      select _role as role, email as email,
         extract(epoch from now())::integer + current_setting('app.jwt_hours')*60*60 as exp
    ) r
    into result;
  return result;
end;
$$;

CREATE TABLE api.messages (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  time         TIMESTAMP NOT NULL DEFAULT now(),
  from_user    NAME      NOT NULL DEFAULT current_user,
  to_user      NAME      NOT NULL,
  subject      VARCHAR(64) NOT NULL,
  body         TEXT
);

CREATE POLICY chat_policy ON api.messages
  USING ((to_user = current_user) OR (from_user = current_user))
  WITH CHECK (from_user = current_user)