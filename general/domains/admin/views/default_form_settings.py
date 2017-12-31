from general.database.session_scope import session_scope


def create_default_form_settings_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_form_settings CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin.default_form_settings AS 
              SELECT coalesce(fs.id, auth.gen_random_uuid()) as id, 
                     u.role as "user",
                     u.id as user_id,
                     f.form_name,
                     f.schema_name,
                     
                     coalesce(fs.custom_button_copy, 'Submit') AS custom_button_copy,
                     coalesce(fs.custom_name, initcap(replace(f.form_name, '_', ' '))) as custom_name,
                     fs.submenu_id,
                     coalesce(fs.icon, 'fa-pencil-square-o') AS icon,
                     coalesce(fs.is_visible, TRUE) AS is_visible, 
                     coalesce(fs.order_index, 99) AS order_index,
                     row_to_json(ds)::JSONB AS dialog_settings

              FROM auth.users u
              LEFT OUTER JOIN admin.forms f
              ON TRUE
              LEFT OUTER JOIN admin.form_settings fs
                  ON f.form_name = fs.form_name
                  AND f.schema_name = fs.schema_name
                  AND u.id = fs.user_id
              LEFT OUTER JOIN admin.dialog_settings ds
                  ON fs.dialog_settings_id = ds.id
                  AND fs.user_id = ds.user_id
              ORDER BY u.role, f.schema_name, f.form_name;
        """)
