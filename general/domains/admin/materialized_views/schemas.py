from general.database.session_scope import session_scope


def create_schemas_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.schemas CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.schemas AS
                SELECT
                   replace(schema_name, '_api', '') AS schema_name
                FROM information_schema.schemata
                WHERE schema_name LIKE '%_api';
        """)


if __name__ == '__main__':
    create_schemas_materialized_view()
