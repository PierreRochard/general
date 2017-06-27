from models.util import session_scope


def create_datatable_columns_function():
    with session_scope() as session:
        session.execute("""
                CREATE OR REPLACE FUNCTION admin.datatable_columns_function()
                  RETURNS TRIGGER AS
                        $BODY$
                           BEGIN
                              IF TG_OP = 'UPDATE' THEN
                                UPDATE admin.table_column_settings SET is_visible=NEW.is_visible
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
