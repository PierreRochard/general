from postgrest_boilerplate.database.util import session_scope


def create_default_form_field_settings_api_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS api.default_form_field_settings CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW api.default_form_field_settings AS 
            SELECT (row_number() OVER())::INT id, *
            FROM (
                      SELECT coalesce(ffs.id, auth.gen_random_uuid()) as id,
                             coalesce(ffs."user", current_user) as "user",
                             f.form_name,
                             unnest(f.form_args) AS form_field_name
                      FROM admin.forms f
                      LEFT OUTER JOIN admin.form_field_settings ffs
                        ON f.form_name = ffs.form_name
                        AND ffs.user = current_user
              ) sub;
        """)

        session.execute("""
         GRANT SELECT ON api.form_field_settings TO anon;
        """)

if __name__ == '__main__':
    create_default_form_field_settings_api_view()
