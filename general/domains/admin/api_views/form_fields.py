from general.database.session_scope import session_scope


def create_form_fields_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.form_fields CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin_api.form_fields AS 
            SELECT (row_number() OVER())::INT id, *
            FROM (
              SELECT 
                     dffs.custom_name,
                     dffs.field_name,
                     dffs.field_type,
                     dffs.form_name,
                     dffs.schema_name,
                     dffs.user_id
              FROM admin.default_form_field_settings dffs
              WHERE dffs."user" = current_user
              ORDER BY dffs.order_index ASC
              ) sub;
        """)

