from postgrest_boilerplate.models.util import session_scope


def create_api_table_settings():
    with session_scope() as session:
        session.execute("""
        CREATE OR REPLACE VIEW api.table_settings AS 
          SELECT coalesce(ts.id, auth.gen_random_uuid()) as id,
                 coalesce(ts."user", current_user) as "user",
                 t.table_name,
                 
                 coalesce(ts.can_delete, TRUE) AS can_delete,
                 coalesce(ts.can_insert, TRUE) AS can_insert,
                 coalesce(ts.can_update, TRUE) AS can_update,
                 coalesce(ts.custom_name, initcap(replace(t.table_name, '_', ' '))) as custom_name,
                 ts.submenu_id,
                 coalesce(ts.icon, 'fa-table') AS icon,
                 coalesce(ts.is_visible, TRUE) AS is_visible,
                 coalesce(ts.order_index, 0) AS order_index,
                 coalesce(ts.row_limit, 10) AS row_limit,
                 coalesce(ts.row_offset, 0) as row_offset,
                 coalesce(ts.sort_column, 'id') as sort_column,
                 coalesce(ts.sort_order, 1) as sort_order
          FROM admin.tables t
          LEFT OUTER JOIN admin.table_settings ts
              ON t.table_name = ts.table_name
              AND ts.user = current_user
          ORDER BY ts.order_index ASC, t.table_name ASC;
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
