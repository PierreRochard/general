from general.database.session_scope import session_scope


def create_default_form_field_settings_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_form_field_settings CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin.default_form_field_settings AS 
              SELECT coalesce(ffs.id, auth.gen_random_uuid()) as id,
                     u.role as "user",
                     u.id as user_id,
                     ff.schema_name,
                     ff.form_name,
                     ff.field_name,
                     
                     ff.field_type,
                     
                     coalesce(ffs.order_index, ff.ordinal_position) AS order_index,
                     coalesce(ffs.custom_name, initcap(replace(ff.field_name, '_', ' '))) as custom_name
              FROM auth.users u
              LEFT OUTER JOIN admin.form_fields ff
                ON TRUE
              LEFT OUTER JOIN admin.form_field_settings ffs
                ON ff.form_name = ffs.form_name
        """)
