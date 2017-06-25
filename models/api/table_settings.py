from models.util import session_scope


def create_api_table_settings():
    with session_scope() as session:
        session.execute("""
        CREATE OR REPLACE VIEW api.table_settings AS 
          SELECT t.table_name, 
                 ts.id,
                 ts.user,
                 ts.custom_name,
                 ts.submenu_id,
                 ts.icon,
                 ts.is_visible,
                 ts.can_insert,
                 ts.can_update,
                 ts.can_delete,
                 ts.order_index,
                 ts.row_limit
          FROM admin.tables t
          LEFT OUTER JOIN admin.table_settings ts
              ON t.table_name = ts.table_name
              AND ts.user = current_user
          ORDER BY ts.order_index ASC NULLS LAST, t.table_name ASC NULLS LAST;
        """)

        session.execute("""
        DROP TRIGGER IF EXISTS table_settings_trigger ON api.table_settings;
        """)

        session.execute("""
        CREATE TRIGGER table_settings_trigger
            INSTEAD OF INSERT OR UPDATE OR DELETE
            ON api.table_settings
            FOR EACH ROW
        EXECUTE PROCEDURE admin.table_settings_function();
        """)

        session.execute("""
        GRANT SELECT ON api.table_settings TO anon;
        """)
