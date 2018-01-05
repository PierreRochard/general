from general.database.session_scope import session_scope


def create_datatable_columns_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.datatable_columns CASCADE;
        """)
        session.execute("""
          CREATE OR REPLACE VIEW admin_api.datatable_columns AS
            SELECT (row_number() OVER())::INT id, *
            FROM (
                    SELECT 
                           dtcs.can_update,
                           dtcs.column_name,
                           dtcs.custom_name,
                           dtcs.data_type,
                           dtcs.filter_match_mode,
                           dtcs.filter_value,
                           dtcs.format_pattern,
                           dtcs.input_type,
                           dtcs.is_filterable,
                           dtcs.is_multiple,
                           dtcs.is_select_item,
                           dtcs.is_sortable,
                           dtcs.is_visible,
                           dtcs.schema_name,
                           dtcs.select_item_schema_name,
                           dtcs.select_item_table_name,
                           dtcs.select_item_label_column_name,
                           dtcs.select_item_value_column_name,
                           dtcs.slice_end,
                           dtcs.slice_start,
                           dtcs.suggestion_column_name,
                           dtcs.suggestion_schema_name,
                           dtcs.suggestion_table_name,
                           dtcs.table_name,
                           dtcs.user_id,
                           json_build_object(
                           'height', dtcs.height,
                           'overflow', dtcs.overflow,
                           'padding-bottom', dtcs.padding_bottom,
                           'padding-left', dtcs.padding_left,
                           'padding-right', dtcs.padding_right,
                           'padding-top', dtcs.padding_top,
                           'width', dtcs.width
                           ) AS styles
                           
                    FROM admin.default_datatable_column_settings dtcs
                  WHERE dtcs.user = current_user
                  ORDER BY dtcs.order_index ASC
          ) sub;
        """)


def create_datatable_columns_trigger():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS admin.datatable_columns_function() CASCADE;
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
          DROP TRIGGER IF EXISTS datatable_columns_trigger ON admin_api.datatable_columns CASCADE;
        """)
        session.execute("""
          CREATE TRIGGER datatable_columns_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON admin_api.datatable_columns
          FOR EACH ROW
          EXECUTE PROCEDURE admin.datatable_columns_function();
        """)

if __name__ == '__main__':
    create_datatable_columns_view()
    create_datatable_columns_trigger()
