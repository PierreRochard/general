import argparse
import os
import subprocess
import sys

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from models import Base
from scripts.setup_login import install_login_function
from scripts.setup_notifications import setup_table_notifications
from scripts.setup_users_table import install_user_table_functions

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
    pg_engine = create_engine(
        f"postgresql+psycopg2://{user}@localhost:5432/postgres", echo=True)
    pg_session = sessionmaker(bind=pg_engine)()
    pg_session.connection().connection.set_isolation_level(0)
    try:
        pg_session.execute(f'CREATE DATABASE {database}')
    except ProgrammingError:
        pg_session.rollback()
    engine = create_engine(
        f'postgresql+psycopg2://{user}@localhost:5432/{database}', echo=True)
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

    install_user_table_functions(session)

    install_login_function(session)
    for schema, table in [('api', 'messages')]:
        setup_table_notifications(session, schema, table)


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description='Install PostgREST Auth')
    argument_parser.add_argument('-d', help='Database name', dest='database')
    argument_parser.add_argument('-u', help='Database user', dest='user')
    args = argument_parser.parse_args()
    install_dependencies()
    setup_database(args.database, args.user)
