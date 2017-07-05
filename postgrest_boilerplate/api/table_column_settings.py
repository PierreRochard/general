from postgrest_boilerplate.models.util import session_scope


def create_api_column_settings():
    with session_scope() as session:
        session.execute("""
        CREATE OR REPLACE VIEW api.table_column_settings AS 
          SELECT coalesce(tcs.id, auth.gen_random_uuid()) as id,
                 coalesce(tcs."user", current_user) as "user",
                 c.table_name,
                 c.column_name,
                 c.is_nullable,
                 c.column_default,
                 c.data_type,
                 
                 coalesce(tcs.can_update, FALSE) as can_update,
                 coalesce(tcs.custom_name, initcap(replace(c.column_name, '_', ' '))) as custom_name,
                 coalesce(tcs.filter_match_mode, 'contains') as filter_match_mode,
                 tcs.filter_value,
                 coalesce(tcs.format_pattern, 
                 CASE WHEN c.data_type = 'timestamp without time zone' THEN 'shortDate'
                      WHEN c.data_type = 'numeric' THEN '1.2-2'
                      ELSE NULL
                  END) as format_pattern,
                 coalesce(tcs.is_filterable, FALSE) as is_filterable,
                 coalesce(tcs.is_sortable, TRUE) as is_sortable,
                 coalesce(tcs.is_visible, TRUE) as is_visible,                
                 coalesce(tcs.order_index, 0) as order_index

          FROM admin.columns c
          LEFT OUTER JOIN admin.table_column_settings tcs
              ON c.table_name = tcs.table_name
              AND c.column_name = tcs.column_name
              AND tcs.user = current_user;
        """)

        session.execute("""
          DROP TRIGGER IF EXISTS column_settings_trigger ON api.table_column_settings;
        """)

        session.execute("""
          CREATE TRIGGER column_settings_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON api.table_column_settings
          FOR EACH ROW
          EXECUTE PROCEDURE admin.table_column_settings_function();
        """)
