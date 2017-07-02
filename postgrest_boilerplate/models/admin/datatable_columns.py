from postgrest_boilerplate.models.util import session_scope


def create_datatable_columns_function():
    with session_scope() as session:
        session.execute("""
                CREATE OR REPLACE FUNCTION admin.datatable_columns_function()
                  RETURNS TRIGGER AS
                        $BODY$
                           BEGIN
                              IF TG_OP = 'UPDATE' THEN
                                INSERT INTO admin.table_column_settings (table_name, column_name, is_visible)
                                VALUES (NEW.table_name, NEW.value, NEW.is_visible)
                                ON CONFLICT ("user", table_name, column_name) 
                                DO UPDATE SET is_visible = NEW.is_visible
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
