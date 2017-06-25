from models.util import session_scope


def create_api_form_settings():
    with session_scope() as session:
        session.execute("""
            CREATE OR REPLACE VIEW api.form_settings AS 
              SELECT f.form_name,
                     f.form_args,
                     f.form_arg_types,
                     fs.id,
                     fs.user,
                    
                     fs.custom_name,
                     fs.submenu_id,
                     fs.icon,
                     fs.is_visible
              FROM admin.forms f
              LEFT OUTER JOIN admin.form_settings fs
                  ON f.form_name = fs.form_name
                  AND fs."user" = current_user;
        """)

        session.execute("""
          DROP TRIGGER IF EXISTS form_settings_trigger ON api.form_settings;
        """)

        session.execute("""
          CREATE TRIGGER form_settings_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON api.form_settings
          FOR EACH ROW
          EXECUTE PROCEDURE admin.form_settings_function();
        """)
