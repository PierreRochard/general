from general.database.util import session_scope


def create_form_fields_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.form_fields CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin_api.form_fields AS 
            SELECT (row_number() OVER())::INT id, *
            FROM (
                      SELECT dffs.form_name,
                             dffs.field_name,
                             dffs.field_type,
                             dffs.custom_name
                      FROM admin.default_form_field_settings dffs
                  WHERE dffs.user = current_user
                  ORDER BY dffs.order_index ASC
              ) sub;
        """)

        session.execute("""
         GRANT SELECT ON admin.default_form_field_settings TO anon;
        """)

if __name__ == '__main__':
    create_form_fields_view()
