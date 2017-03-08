import argparse
import os
import subprocess
import sys

# git clone https://github.com/michelp/pgjwt
# cd pgjwt
# make install
from models import get_session

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
    session = get_session(database, user)
    secret = '4S7lR9SnY8g3'
    hours = 24
    session.execute(f"""
    ALTER DATABASE {database} SET "app.jwt_secret" TO '{secret}';
    ALTER DATABASE {database} SET "app.jwt_hours" TO {hours};

    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    CREATE EXTENSION IF NOT EXISTS pgjwt;

    CREATE SCHEMA IF NOT EXISTS auth;
    CREATE SCHEMA IF NOT EXISTS api;

    CREATE ROLE anon;
    CREATE ROLE authenticator NOINHERIT;
    GRANT anon TO authenticator;

    GRANT USAGE ON SCHEMA api, auth TO anon;
    GRANT EXECUTE ON FUNCTION api.login(TEXT, TEXT) TO anon;
    """)


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='Install PostgREST Auth')
    argument_parser.add_argument('-d',  help='Database name', dest='database')
    argument_parser.add_argument('-u',  help='Database user', dest='user')
    args = argument_parser.parse_args()
    install_dependencies()
    setup_database(args.database, args.user)
