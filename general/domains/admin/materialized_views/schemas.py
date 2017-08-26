from general.database.util import session_scope


def create_schemas_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.schemas CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.schemas AS
                SELECT
                   schema_name
                FROM information_schema.schemata
                WHERE schema_name LIKE '%_api';
        """)


if __name__ == '__main__':
    create_schemas_materialized_view()
