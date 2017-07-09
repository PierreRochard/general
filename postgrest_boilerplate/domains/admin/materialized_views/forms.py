from postgrest_boilerplate.database.util import session_scope


def create_forms_admin_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.forms CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.forms AS
                SELECT pg_proc.proname as form_name,
                       pg_proc.proargnames as form_args,
                       pg_proc.proargtypes AS form_arg_types
                FROM pg_proc
                LEFT OUTER JOIN pg_namespace ON pg_namespace.OID = pg_proc.pronamespace
                WHERE pg_namespace.nspname = 'api';
        """)

if __name__ == '__main__':
    create_forms_admin_materialized_view()