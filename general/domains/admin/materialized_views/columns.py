from general.database.util import session_scope


def create_columns_admin_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.columns CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.columns AS
                SELECT table_name, 
                       column_name, 
                       is_nullable,
                       column_default,
                       data_type
                FROM information_schema.columns
                WHERE table_schema LIKE '%api'
                  AND column_name NOT LIKE '%_select_items';
    
        """)


if __name__ == '__main__':
    create_columns_admin_materialized_view()
