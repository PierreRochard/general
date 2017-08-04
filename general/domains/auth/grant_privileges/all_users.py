from general.database.util import session_scope
from general.domains.auth.models import Users


def grant_privileges_to_anon():
    with session_scope(raise_programming_error=True) as session:
        session.execute('GRANT USAGE ON SCHEMA api TO anon;')
        session.execute('GRANT SELECT ON TABLE auth.users TO anon;')


def grant_privileges_to_users():
    with session_scope(raise_programming_error=True) as session:
        for role_name, in session.query(Users.role).all():
            session.execute(f'GRANT USAGE ON SCHEMA api TO "{role_name}";')

if __name__ == '__main__':
    grant_privileges_to_users()
