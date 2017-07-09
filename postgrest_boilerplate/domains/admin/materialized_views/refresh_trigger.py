from postgrest_boilerplate.database.util import session_scope


def create_materialized_views_refresh_trigger():
    with session_scope() as session:
        session.execute("""
            CREATE OR REPLACE FUNCTION admin.refresh_admin_views()
              RETURNS event_trigger AS
                    $BODY$
                       BEGIN
                       REFRESH MATERIALIZED VIEW admin.tables;
                       REFRESH MATERIALIZED VIEW admin.columns;
                       REFRESH MATERIALIZED VIEW admin.forms;
                       END;
                    $BODY$
              LANGUAGE plpgsql VOLATILE
              COST 100;
        """)

        session.execute("""
          DROP EVENT TRIGGER IF EXISTS refresh_admin_tables_trigger;
        """)

        session.execute("""
            CREATE EVENT TRIGGER refresh_admin_tables_trigger
              ON ddl_command_end
              WHEN tag IN (
                    'ALTER FUNCTION',
                    'CREATE FUNCTION',
                    'DROP FUNCTION',
                    'ALTER VIEW',
                    'CREATE VIEW',
                    'DROP VIEW',
                    'ALTER TABLE',
                    'CREATE TABLE', 
                    'CREATE TABLE AS',
                    'DROP TABLE')
              EXECUTE PROCEDURE admin.refresh_admin_tables();
        """)

        session.execute("""
                REFRESH MATERIALIZED VIEW admin.tables;
                REFRESH MATERIALIZED VIEW admin.columns;
                REFRESH MATERIALIZED VIEW admin.forms;
                """)

if __name__ == '__main__':
    create_materialized_views_refresh_trigger()
