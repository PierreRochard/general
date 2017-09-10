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
                SELECT dts.custom_name AS "customName",
                       dts.order_index AS "orderIndex",
                       dts.row_limit AS "rowLimit",
                       dts.row_offset AS "rowOffset",
                       dts.schema_name AS "schemaName",
                       dts.sort_column AS "sortColumn",
                       dts.sort_order AS "sortOrder",
                       dts.table_name AS "tableName",
                       dts.user_id AS "userId"
                FROM admin.default_datatable_settings dts
                WHERE dts."user" = current_user
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
                          INSERT INTO admin.table_settings (
                          custom_name,
                          order_index,
                          row_limit, 
                          row_offset, 
                          schema_name, 
                          sort_column, 
                          sort_order, 
                          table_name,
                          user_id
                          )
                          VALUES (
                          NEW."customName",
                          NEW."orderIndex",
                          NEW."rowLimit",
                          NEW."rowOffset", 
                          NEW."schemaName", 
                          NEW."sortColumn", 
                          NEW."sortOrder",
                          NEW."tableName",
                          NEW."userId"
                          )
                          ON CONFLICT (user_id, schema_name, table_name)
                            DO UPDATE SET 
                                   row_offset=NEW."offset",
                                   sort_column=NEW."sortColumn",
                                   sort_order=NEW."sortOrder"
                            WHERE admin.table_settings.user_id = NEW.userId
                              AND admin.table_settings.table_name = NEW.tableName
                              AND admin.table_settings.schema_name = NEW.schemaName;
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
