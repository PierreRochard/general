from general.database.session_scope import session_scope


def create_datatables_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.datatables CASCADE;
        """)
        session.execute("""
          CREATE OR REPLACE VIEW admin_api.datatables AS
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


def create_datatables_trigger():
    with session_scope() as session:
        session.execute("""
            DROP FUNCTION IF EXISTS admin.datatables_function() CASCADE;
        """)

        session.execute("""
            CREATE OR REPLACE FUNCTION admin.datatables_function()
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
          DROP TRIGGER IF EXISTS datatables_trigger ON admin_api.datatables;
        """)

        session.execute("""
          CREATE TRIGGER datatables_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON admin_api.datatables
          FOR EACH ROW
          EXECUTE PROCEDURE admin.datatables_function();
        """)

if __name__ == '__main__':
    create_datatables_view()
    create_datatables_trigger()
