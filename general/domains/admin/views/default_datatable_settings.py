from general.database.session_scope import session_scope


def create_default_datatable_settings_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_datatable_settings CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin.default_datatable_settings AS 
          SELECT coalesce(ts.id, auth.gen_random_uuid()) as id,
                 u.role as "user",
                 u.id as user_id,
                 t.schema_name,
                 t.table_name,
                 
                 coalesce(ts.can_archive, FALSE) AS can_archive,
                 coalesce(ts.can_delete, FALSE) AS can_delete,
                 coalesce(ts.can_insert, FALSE) AS can_insert,
                 coalesce(ts.can_update, TRUE) AS can_update,
                 coalesce(ts.custom_name, initcap(replace(t.table_name, '_', ' '))) as custom_name,
                 ts.submenu_id,
                 coalesce(ts.icon, 'fa-table') AS icon,
                 coalesce(ts.is_visible, FALSE) AS is_visible,
                 coalesce(ts.order_index, 0) AS order_index,
                 coalesce(ts.row_limit, 10) AS row_limit,
                 coalesce(ts.row_offset, 0) as row_offset,
                 coalesce(ts.sort_column, 'id') as sort_column,
                 coalesce(ts.sort_order, 1) as sort_order,
                 ts.mapping_column_name,
                 ts.mapping_table_name,
                 ts.mapping_schema_name,
                 ts.keyword_column_name
          FROM auth.users u
          LEFT OUTER JOIN admin.tables t
          ON TRUE 
          LEFT OUTER JOIN admin.table_settings ts
              ON t.schema_name = ts.schema_name
              AND t.table_name = ts.table_name
              AND u.id = ts.user_id
          ORDER BY u.role, t.schema_name, t.table_name;
        """)
