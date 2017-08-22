from general.database.util import session_scope


def create_default_datatable_column_settings_api_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_datatable_column_settings CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin.default_datatable_column_settings AS 
          SELECT coalesce(tcs.id, auth.gen_random_uuid()) as id,
                 coalesce(u.role, current_user) as "user",
                 c.table_name,
                 c.column_name,
                 c.is_nullable,
                 c.column_default,
                 c.data_type,
                 
                 coalesce(tcs.can_update, FALSE) as can_update,
                 coalesce(tcs.custom_name, initcap(replace(c.column_name, '_', ' '))) as custom_name,
                 coalesce(tcs.filter_match_mode, 'contains') as filter_match_mode,
                 tcs.filter_value,
                 coalesce(tcs.format_pattern, 
                 CASE WHEN c.data_type = 'timestamp without time zone' THEN 'shortDate'
                      WHEN c.data_type = 'numeric' THEN '1.2-2'
                      ELSE NULL
                  END) as format_pattern,
                 coalesce(tcs.input_type, 'text') as input_type,
                 coalesce(tcs.is_filterable, FALSE) as is_filterable,
                 coalesce(tcs.is_sortable, TRUE) as is_sortable,
                 coalesce(tcs.is_visible, TRUE) as is_visible,                
                 coalesce(tcs.order_index, 0) as order_index

          FROM admin.columns c
          LEFT OUTER JOIN admin.table_column_settings tcs
              ON c.table_name = tcs.table_name
              AND c.column_name = tcs.column_name
          LEFT JOIN auth.users u 
            ON tcs.user_id = u.id
        """)


def create_default_datatable_column_settings_api_trigger():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS admin.datatable_column_settings_function() CASCADE;
        """)

        session.execute("""
        CREATE OR REPLACE FUNCTION admin.datatable_column_settings_function()
          RETURNS TRIGGER AS
                $BODY$
                   BEGIN
                    IF TG_OP = 'INSERT' THEN
                        INSERT INTO admin.table_column_settings 
                                              (table_name,
                                               column_name,
                                               
                                               can_update,
                                               custom_name,
                                               format,
                                               index,
                                               is_visible) 
                                      VALUES(NEW.table_name,
                                             NEW.column_name,
                                             
                                             NEW.can_update,
                                             NEW.custom_name,
                                             NEW.format,
                                             NEW.index,
                                             NEW.is_visible);
                        RETURN NEW;
                      ELSIF TG_OP = 'UPDATE' THEN
                        UPDATE admin.table_column_settings SET 
                               can_update=NEW.can_update,
                               custom_name=NEW.custom_name,
                               format=NEW.format,
                               index=NEW.index,
                               is_visible=NEW.is_visible  
                            WHERE id=OLD.id;
                       RETURN NEW;
                      ELSIF TG_OP = 'DELETE' THEN
                       DELETE 
                          FROM admin.table_column_settings 
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
          DROP TRIGGER IF EXISTS default_datatable_column_settings_trigger ON api.default_datatable_column_settings;
        """)

        session.execute("""
          CREATE TRIGGER default_datatable_column_settings_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON api.default_datatable_column_settings
          FOR EACH ROW
          EXECUTE PROCEDURE admin.datatable_column_settings_function();
        """)

if __name__ == '__main__':
    create_default_datatable_column_settings_api_view()
    create_default_datatable_column_settings_api_trigger()
