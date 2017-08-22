from general.database.util import session_scope


def create_datatable_api_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.datatable CASCADE;
        """)
        session.execute("""
          CREATE OR REPLACE VIEW admin_api.datatable AS
            SELECT (row_number() OVER())::INT id, *
            FROM (
                SELECT dts.table_name AS name, 
                       dts.custom_name AS header,
                       dts.row_limit AS "limit",
                       dts.row_offset AS "offset",
                       dts.sort_column,
                       dts.sort_order,
                       dts.order_index
                FROM admin.default_datatable_settings dts
                WHERE dts.user = current_user
            ) sub;
        """)


def create_datatable_api_trigger():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS admin.datatable_function() CASCADE;
        """)

        session.execute("""
            CREATE OR REPLACE FUNCTION admin.datatable_function()
              RETURNS TRIGGER AS
                    $BODY$
                       BEGIN
                          IF TG_OP = 'UPDATE' THEN
                          INSERT INTO admin.table_settings (table_name, row_offset, sort_column, sort_order)
                          VALUES (NEW.name, NEW."offset", NEW.sort_column, NEW.sort_order)
                          ON CONFLICT ("user", table_name)
                            DO UPDATE SET 
                                   row_offset=NEW."offset",
                                   sort_column=NEW.sort_column,
                                   sort_order=NEW.sort_order
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

        session.execute("""
          DROP TRIGGER IF EXISTS datatable_trigger ON api.datatable;
        """)

        session.execute("""
          CREATE TRIGGER datatable_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON api.datatable
          FOR EACH ROW
          EXECUTE PROCEDURE admin.datatable_function();
        """)

if __name__ == '__main__':
    create_datatable_api_view()
    create_datatable_api_trigger()
