from general.database.util import session_scope


def create_tables_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.tables CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.tables AS
                SELECT
                   pg_class.relname AS "table_name", 
                   pg_class.relkind AS "kind",
                   reltuples AS "row_count" 
                FROM pg_class
                  JOIN pg_namespace ON 	pg_namespace.oid = pg_class.relnamespace
                WHERE pg_namespace.nspname = 'api' 
                AND pg_class.relkind IN ('v', 'm', 'r');
        """)


if __name__ == '__main__':
    create_tables_materialized_view()
