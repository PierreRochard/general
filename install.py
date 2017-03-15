import argparse
import os
import subprocess
import sys

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from models.admin import Users, Messages
from models.postgrest import Settings
from models import Base


python = sys.executable


def run_command(command, cwd=None):
    print(subprocess.Popen(command, stdout=subprocess.PIPE,
                           cwd=cwd).stdout.read())


def install_dependencies():
    library_directory = os.path.join(os.path.dirname(__file__), 'libraries')
    if not os.path.exists(library_directory):
        os.mkdir(library_directory)

    run_command(['git', 'pull'])
    run_command(['pip', '--no-cache-dir', 'install', '--upgrade', '-r',
                 'requirements.txt'])

    custom_repos = [{'package': 'pgjwt',
                     'url': 'https://github.com/michelp/pgjwt',
                     'branch': None},
                    ]
    for repo in custom_repos:
        directory = os.path.join(library_directory, repo['package'])
        if not os.path.exists(directory):
            run_command(['git', 'clone', repo['url'], directory])
            if repo['branch']:
                run_command(['git', 'checkout', repo['branch']],
                            cwd=directory)
        else:
            if repo['branch']:
                run_command(['git', 'checkout', repo['branch']],
                            cwd=directory)
            run_command(['git', 'pull'], cwd=directory)
        if os.path.exists(os.path.join(directory, 'setup.py')):
            run_command([python, 'setup.py', 'install'], cwd=directory)
        else:
            run_command(['make', 'install'], cwd=directory)


def setup_database(database, user):
    pg_engine = create_engine(f"postgresql+psycopg2://{user}@localhost:5432/postgres", echo=True)
    pg_session = sessionmaker(bind=pg_engine)()
    pg_session.connection().connection.set_isolation_level(0)
    try:
        pg_session.execute(f'CREATE DATABASE {database}')
    except ProgrammingError:
        pg_session.rollback()
    engine = create_engine(f'postgresql+psycopg2://{user}@localhost:5432/{database}', echo=True)
    session = scoped_session(sessionmaker(bind=engine, autocommit=True))()
    session.connection().connection.set_isolation_level(0)
    secret = '4S7lR9SnY8g3'
    hours = 24
    try:
        session.execute("""
        CREATE ROLE anon;
        """)
    except ProgrammingError:
        session.rollback()
    try:
        session.execute("""
        CREATE ROLE authenticator NOINHERIT;
        GRANT anon TO authenticator;
        """)
    except ProgrammingError:
        session.rollback()

    session.execute(f"""
    ALTER DATABASE {database} SET "app.jwt_secret" TO '{secret}';
    ALTER DATABASE {database} SET "app.jwt_hours" TO {hours};

    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    CREATE EXTENSION IF NOT EXISTS pgjwt;

    CREATE SCHEMA IF NOT EXISTS admin;
    CREATE SCHEMA IF NOT EXISTS api;
    CREATE SCHEMA IF NOT EXISTS auth;

    GRANT USAGE ON SCHEMA api, auth TO anon;
    """)

    Base.metadata.create_all(bind=engine)

    try:
        session.execute("""
        CREATE TYPE auth.jwt_token AS (
        token TEXT
        );
        """)
    except ProgrammingError:
        session.rollback()

    session.execute("GRANT SELECT ON TABLE auth.users TO anon;")

    session.execute(f"""
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

    session.execute(f"""
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
    """)
    session.execute('''
    GRANT EXECUTE ON FUNCTION api.login(TEXT, TEXT) TO anon;
    ''')

if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='Install PostgREST Auth')
    argument_parser.add_argument('-d',  help='Database name', dest='database')
    argument_parser.add_argument('-u',  help='Database user', dest='user')
    args = argument_parser.parse_args()
    install_dependencies()
    setup_database(args.database, args.user)
