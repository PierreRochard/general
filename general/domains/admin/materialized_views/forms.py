from general.database.session_scope import session_scope


def create_forms_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.forms CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.forms AS
                SELECT replace(specific_schema, '_api', '') AS schema_name,
                       routine_name as form_name
                FROM information_schema.routines
                WHERE specific_schema LIKE '%_api';
        """)

if __name__ == '__main__':
    create_forms_materialized_view()
