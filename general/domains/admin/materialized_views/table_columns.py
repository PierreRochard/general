from general.database.session_scope import session_scope


def create_table_columns_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.table_columns CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.table_columns AS
                SELECT table_schema as schema_name,
                       table_name, 
                       column_name, 
                       is_nullable,
                       column_default,
                       data_type
                FROM information_schema.columns
                WHERE table_schema LIKE '%_api'
                  AND column_name NOT LIKE '%_select_items';
        """)


if __name__ == '__main__':
    create_table_columns_materialized_view()
