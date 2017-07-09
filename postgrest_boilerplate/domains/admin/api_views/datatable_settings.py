from postgrest_boilerplate.database.util import session_scope


def create_datatable_settings_api_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS api.datatable_settings CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW api.datatable_settings AS 
          SELECT coalesce(ts.id, auth.gen_random_uuid()) as id,
                 coalesce(ts."user", current_user) as "user",
                 t.table_name,
                 
                 coalesce(ts.can_delete, TRUE) AS can_delete,
                 coalesce(ts.can_insert, TRUE) AS can_insert,
                 coalesce(ts.can_update, TRUE) AS can_update,
                 coalesce(ts.custom_name, initcap(replace(t.table_name, '_', ' '))) as custom_name,
                 ts.submenu_id,
                 coalesce(ts.icon, 'fa-table') AS icon,
                 coalesce(ts.is_visible, TRUE) AS is_visible,
                 coalesce(ts.order_index, 0) AS order_index,
                 coalesce(ts.row_limit, 10) AS row_limit,
                 coalesce(ts.row_offset, 0) as row_offset,
                 coalesce(ts.sort_column, 'id') as sort_column,
                 coalesce(ts.sort_order, 1) as sort_order
          FROM admin.tables t
          LEFT OUTER JOIN admin.table_settings ts
              ON t.table_name = ts.table_name
              AND ts.user = current_user
          ORDER BY ts.order_index ASC, t.table_name ASC;
        """)


def create_datatable_settings_api_trigger():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS admin.datatable_settings_function() CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE FUNCTION admin.datatable_settings_function()
              RETURNS TRIGGER AS
                    $BODY$
                       BEGIN
                        IF TG_OP = 'INSERT' THEN
                            INSERT INTO admin.table_settings 
                                                (table_name,
                                                  can_delete,
                                                  can_insert,
                                                  can_update,
                                                  custom_name,
                                                  submenu_id,
                                                  icon,
                                                  is_visible) 
                                          VALUES(NEW.table_name,
                                                 NEW.can_delete,
                                                 NEW.can_insert,
                                                 NEW.can_update,
                                                 NEW.custom_name,
                                                 NEW.submenu_id,
                                                 NEW.icon,
                                                 NEW.is_visible);
                            RETURN NEW;
                          ELSIF TG_OP = 'UPDATE' THEN
                              UPDATE admin.table_settings SET 
                                     can_delete=NEW.can_delete, 
                                     can_insert=NEW.can_insert, 
                                     can_update=NEW.can_update, 
                                     custom_name=NEW.custom_name, 
                                     submenu_id=NEW.submenu_id, 
                                     icon=NEW.icon, 
                                     is_visible=NEW.is_visible 
                              WHERE id=OLD.id;
                           RETURN NEW;
                          ELSIF TG_OP = 'DELETE' THEN
                           DELETE 
                             FROM admin.table_settings 
                           WHERE id=OLD.id;
                           RETURN NULL; 
                        END IF;
                        RETURN NEW;
                      END;
                    $BODY$
              LANGUAGE plpgsql VOLATILE
              COST 100;
                """)

        session.execute("""
          DROP TRIGGER IF EXISTS datatable_settings_trigger ON api.datatable_settings CASCADE;
        """)
        session.execute("""
        CREATE TRIGGER datatable_settings_trigger
            INSTEAD OF INSERT OR UPDATE OR DELETE
            ON api.datatable_settings
            FOR EACH ROW
        EXECUTE PROCEDURE admin.datatable_settings_function();
        """)


if __name__ == '__main__':
    create_datatable_settings_api_view()
    create_datatable_settings_api_trigger()
