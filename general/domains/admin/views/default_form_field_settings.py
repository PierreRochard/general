from general.database.util import session_scope


def create_default_form_field_settings_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_form_field_settings CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin.default_form_field_settings AS 
              SELECT coalesce(ffs.id, auth.gen_random_uuid()) as id,
                     coalesce(u.role, current_user) as "user",
                     f.form_name,
                     f.field_name,
                     f.field_type,
                     
                     coalesce(ffs.order_index, 0) AS order_index,
                     coalesce(ffs.custom_name, initcap(replace(f.field_name, '_', ' '))) as custom_name
              FROM admin.fields f
              LEFT OUTER JOIN admin.form_field_settings ffs
                ON f.form_name = ffs.form_name
              LEFT JOIN auth.users u 
                ON ffs.user_id = u.id;
        """)

        session.execute("""
         GRANT SELECT ON admin.default_form_field_settings TO anon;
        """)

if __name__ == '__main__':
    create_default_form_field_settings_view()
