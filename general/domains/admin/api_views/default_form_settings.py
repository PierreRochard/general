from general.database.util import session_scope


def create_form_settings_api_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS api.form_settings CASCADE;
        """)
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
         GRANT SELECT ON api.form_settings TO anon;
        """)


def create_form_settings_api_trigger():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS admin.form_settings_function() CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE FUNCTION admin.form_settings_function()
          RETURNS TRIGGER AS
                $BODY$
                   BEGIN
                    IF TG_OP = 'INSERT' THEN
                        INSERT INTO admin.form_settings (form_name,
    
                                                           custom_name,
                                                           submenu_id,
                                                           icon,
                                                           is_visible)
                                                  VALUES(NEW.form_name,
    
                                                         NEW.custom_name,
                                                         NEW.submenu_id,
                                                         NEW.icon,
                                                         NEW.is_visible);
                        RETURN NEW;
                      ELSIF TG_OP = 'UPDATE' THEN
                       --UPDATE person_detail SET pid=NEW.pid, pname=NEW.pname WHERE pid=OLD.pid;
                       --UPDATE person_job SET pid=NEW.pid, job=NEW.job WHERE pid=OLD.pid;
                       RETURN NEW;
                      ELSIF TG_OP = 'DELETE' THEN
                       --DELETE FROM person_job WHERE pid=OLD.pid;
                       --DELETE FROM person_detail WHERE pid=OLD.pid;
                       RETURN NULL;
                    END IF;
                    RETURN NEW;
                  END;
                $BODY$
          LANGUAGE plpgsql VOLATILE
          COST 100;
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

if __name__ == '__main__':
    create_form_settings_api_view()
    create_form_settings_api_trigger()
