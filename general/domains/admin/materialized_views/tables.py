from general.database.session_scope import session_scope


def create_tables_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.tables CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.tables AS
                SELECT
                   table_schema AS schema_name,
                   table_name,
                   table_type
                FROM information_schema.tables
                WHERE table_schema LIKE '%_api';
        """)


if __name__ == '__main__':
    create_tables_materialized_view()
