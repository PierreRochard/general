from models.util import session_scope


def create_datatable_function():
    with session_scope() as session:
        session.execute("""
                CREATE OR REPLACE FUNCTION admin.datatable_function()
                  RETURNS TRIGGER AS
                        $BODY$
                           BEGIN
                              IF TG_OP = 'UPDATE' THEN
                                UPDATE admin.table_settings SET row_offset=NEW.offset
                                WHERE admin.table_settings.user = current_user
                                  AND admin.table_settings.table_name = NEW.name;
                               RETURN NEW;
                            END IF;
                            RETURN NEW;
                          END;
                        $BODY$
                  LANGUAGE plpgsql VOLATILE
                  COST 100;
                """)
