from general.database.session_scope import session_scope


def create_default_datatable_column_settings_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_datatable_column_settings CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin.default_datatable_column_settings AS 
          SELECT coalesce(tcs.id, auth.gen_random_uuid()) as id,
                 u.role as "user",
                 u.id as user_id,
                 tc.schema_name,
                 tc.table_name,
                 tc.column_name,
                 
                 tc.is_nullable,
                 tc.column_default,
                 tc.data_type,
                 
                 coalesce(tcs.can_update, FALSE) as can_update,
                 coalesce(tcs.custom_name, initcap(replace(tc.column_name, '_', ' '))) as custom_name,
                 coalesce(tcs.filter_match_mode, 'contains') as filter_match_mode,
                 tcs.filter_value,
                 coalesce(tcs.format_pattern, 
                 CASE WHEN tc.data_type = 'timestamp without time zone' THEN 'shortDate'
                      WHEN tc.data_type = 'numeric' THEN '1.2-2'
                      ELSE NULL
                  END) as format_pattern,
                 coalesce(tcs.input_type, 'text') as input_type,
                 coalesce(tcs.is_filterable, FALSE) as is_filterable,
                 coalesce(tcs.is_multiple, FALSE) as is_multiple,
                 coalesce(tcs.is_select_item, FALSE) as is_select_item,
                 coalesce(tcs.is_sortable, TRUE) as is_sortable,
                 coalesce(tcs.is_visible, TRUE) as is_visible,
                 tcs.select_item_label_column_name,
                 tcs.select_item_schema_name,
                 tcs.select_item_table_name,
                 tcs.select_item_value_column_name,
                 tcs.suggestion_column_name,
                 tcs.suggestion_schema_name,
                 tcs.suggestion_table_name,
                 coalesce(tcs.order_index, 0) as order_index,
                 CASE WHEN tcs.height IS NULL THEN 'auto' ELSE concat(tcs.height, 'px') END as height,
                 coalesce(tcs.overflow, 'visible') as overflow,
                 CASE WHEN tcs.padding_bottom IS NULL THEN 'auto' ELSE concat(tcs.padding_bottom, 'px') END as padding_bottom,
                 CASE WHEN tcs.padding_left IS NULL THEN 'auto' ELSE concat(tcs.padding_left, 'px') END as padding_left,
                 CASE WHEN tcs.padding_right IS NULL THEN 'auto' ELSE concat(tcs.padding_right, 'px') END as padding_right,
                 CASE WHEN tcs.padding_top IS NULL THEN 'auto' ELSE concat(tcs.padding_top, 'px') END as padding_top,
                 concat(coalesce(tcs.width, 200), 'px') AS width
          FROM auth.users u
          LEFT OUTER JOIN admin.table_columns tc
            ON TRUE
          LEFT OUTER JOIN admin.table_column_settings tcs
              ON  tc.schema_name = tcs.schema_name
              AND tc.table_name = tcs.table_name
              AND tc.column_name = tcs.column_name
          ORDER BY u.role, tc.schema_name, tc.table_name
        """)
