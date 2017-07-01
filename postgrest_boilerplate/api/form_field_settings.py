from postgrest_boilerplate.models.util import session_scope


def create_api_form_field_settings():
    with session_scope() as session:
        session.execute("""
            CREATE OR REPLACE VIEW api.form_field_settings AS 
              SELECT f.form_name,
                     unnest(f.form_args) as form_field_name
              FROM admin.forms f;
        """)

        session.execute("""
         GRANT SELECT ON api.form_field_settings TO anon;
        """)
