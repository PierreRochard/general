from general.database.util import session_scope


def create_default_form_field_settings_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_form_field_settings CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin.default_form_field_settings AS 
            SELECT (row_number() OVER())::INT id, *
            FROM (
                      SELECT coalesce(u.role, current_user) as "user",
                             f.form_name,
                             unnest(f.form_args) AS form_field_name
                      FROM admin.forms f
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
