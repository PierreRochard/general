from postgrest_boilerplate.database.util import session_scope


def create_admin_tables_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.tables CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.tables AS
                SELECT pg_class.relname AS "table_name", 
                       pg_class.relkind AS "kind",
                       reltuples AS "row_count" 
                FROM pg_class
                  JOIN pg_namespace ON 	pg_namespace.oid = pg_class.relnamespace
                WHERE pg_namespace.nspname = 'api' 
                AND pg_class.relkind IN ('v', 'm', 'r');
        """)

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

        # Create default settings records
        # session.execute("""
        #     CREATE OR REPLACE FUNCTION admin.create_defaults_function()
        #     RETURNS VOID AS $$
        #       DECLARE
        #       pg_users RECORD[];
        #       tables RECORD[];
        #       BEGIN
        #         SELECT information_schema
        #         <<users_loop>>
        #         FOREACH pg_user IN ARRAY pg_users
        #           LOOP
        #             <<periods_loop>>
        #              FOR period_name in SELECT DISTINCT
        #                       to_char(bookkeeping.journal_entries.timestamp,
        #                       period_interval_name) AS p
        #                 FROM bookkeeping.journal_entries
        #                 WHERE bookkeeping.journal_entries.timestamp >= new.timestamp LOOP
        #               PERFORM bookkeeping.update_trial_balance(
        #                     new.debit_subaccount,
        #                     period_interval_name,
        #                     period_name.p);
        #               PERFORM bookkeeping.update_trial_balance(
        #                     new.credit_subaccount,
        #                     period_interval_name,
        #                     period_name.p);
        #             END LOOP periods_loop;
        #           END LOOP period_interval_loop;
        #         RETURN new;
        #       END;
        #     $$
        #     SECURITY DEFINER
        #     LANGUAGE  plpgsql;
        #     """)
