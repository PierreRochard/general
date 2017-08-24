from general.database.util import session_scope


def create_form_fields_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.form_fields CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin.form_fields AS 
            SELECT (row_number() OVER())::INT id, *
            FROM (
                      SELECT dfs.form_name,
                             dfs.
                      FROM admin.default_form_settings. dfs
                      LEFT OUTER JOIN admin.form_field_settings ffs
                        ON f.form_name = ffs.form_name
                      LEFT JOIN auth.users u 
                        ON ffs.user_id = u.id 
              ) sub;
        """)

        session.execute("""
         GRANT SELECT ON admin.default_form_field_settings TO anon;
        """)

if __name__ == '__main__':
    create_default_form_field_settings_view()
