from postgrest_boilerplate.database.util import session_scope
from postgrest_boilerplate.domains.auth.models import Users


def grant_admin_schema_privileges_to_users():
    with session_scope(raise_programming_error=True) as session:
        for user in session.query(Users).all():
            for schema in ['admin', 'auth']:
                session.execute(f'GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA {schema} TO "{user.role}";')
                session.execute(f'GRANT USAGE ON SCHEMA {schema} TO "{user.role}";')
            session.execute(f'GRANT SELECT ON api.menubar TO "{user.role}";')
            session.execute(f'GRANT SELECT ON api.items TO "{user.role}";')
            session.execute(f'GRANT SELECT, UPDATE ON api.datatable TO "{user.role}";')
            session.execute(f'GRANT SELECT, UPDATE ON api.datatable_columns TO "{user.role}";')

if __name__ == '__main__':
    grant_admin_schema_privileges_to_users()
