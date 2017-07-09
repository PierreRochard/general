from postgrest_boilerplate.database.util import session_scope


def create_datatable_columns_api_view():
    with session_scope() as session:
        session.execute("""
          CREATE OR REPLACE VIEW api.datatable_columns AS
            SELECT (row_number() OVER())::INT id, *
            FROM (
                    SELECT tcs.data_type,
                           tcs.filter_match_mode,
                           tcs.filter_value,
                           tcs.format_pattern,
                           tcs.is_filterable,
                           tcs.is_sortable,
                           tcs.is_visible,
                           tcs.custom_name AS label,
                           tcs.table_name,
                           tcs.column_name AS value,
                           tcs.can_update as editable
                           
                    FROM api.table_column_settings tcs
                  ORDER BY order_index ASC
          ) sub;
        """)

        session.execute("""
         GRANT SELECT ON api.datatable_columns TO anon;
        """)


def create_datatable_columns_api_trigger():
    with session_scope() as session:
        session.execute("""
          DROP TRIGGER IF EXISTS datatable_columns_trigger ON api.datatable_columns;
        """)

        session.execute("""
            CREATE OR REPLACE FUNCTION admin.datatable_columns_function()
              RETURNS TRIGGER AS
                $BODY$
                   BEGIN
                      IF TG_OP = 'UPDATE' THEN
                        INSERT INTO admin.table_column_settings
                            (table_name, 
                             column_name, 
                             is_visible, 
                             can_update)
                        VALUES 
                            (NEW.table_name, 
                            NEW.value, 
                            NEW.is_visible, 
                            NEW.editable)
                        ON CONFLICT ("user", table_name, column_name) 
                        DO UPDATE SET is_visible = NEW.is_visible,
                                      can_update = NEW.editable
                            WHERE admin.table_column_settings.user = current_user
                              AND admin.table_column_settings.table_name = NEW.table_name
                              AND admin.table_column_settings.column_name = NEW.value;
                       RETURN NEW;
                    END IF;
                    RETURN NEW;
                  END;
                $BODY$
              LANGUAGE plpgsql VOLATILE
              COST 100;
                        """)

        session.execute("""
          CREATE TRIGGER datatable_columns_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON api.datatable_columns
          FOR EACH ROW
          EXECUTE PROCEDURE admin.datatable_columns_function();
        """)
