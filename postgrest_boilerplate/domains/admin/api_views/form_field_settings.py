from postgrest_boilerplate.database.util import session_scope


def create_form_field_settings_api_view():
    with session_scope() as session:
        session.execute("""
            CREATE OR REPLACE VIEW api.form_field_settings AS 
            SELECT (row_number() OVER())::INT id, *
            FROM (
                      SELECT f.form_name,
                             unnest(f.form_args) AS form_field_name
                      FROM admin.forms f
              ) sub;
        """)

        session.execute("""
         GRANT SELECT ON api.form_field_settings TO anon;
        """)
