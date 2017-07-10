from postgrest_boilerplate.database.util import session_scope


def create_fields_admin_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.fields CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.forms AS
                SELECT pg_proc.proname as form_name,
                       unnest(pg_proc.proargnames, pg_proc.proargtypes),
                FROM pg_proc
                LEFT OUTER JOIN pg_namespace ON pg_namespace.OID = pg_proc.pronamespace
                WHERE pg_namespace.nspname = 'api';
        """)

if __name__ == '__main__':
    create_fields_admin_materialized_view()

# SELECT (row_number() OVER())::INT id, sub1.* FROM
# (SELECT pg_proc.proname as form_name,
#                            unnest(pg_proc.proargnames) as name
# FROM pg_catalog.pg_proc) sub1
# ;