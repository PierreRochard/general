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
                SELECT 
                       dts.can_archive,
                       dts.can_delete,
                       dts.custom_name,
                       dts.order_index,
                       dts.row_limit,
                       dts.row_offset,
                       dts.schema_name,
                       dts.sort_column,
                       dts.sort_order,
                       dts.table_name,
                       dts.user_id,
                       coalesce(fc.filter_columns, '[]') AS filter_columns
                FROM admin.default_datatable_settings dts
                LEFT OUTER JOIN (
                  SELECT
                    dc.table_name,
                    dc.schema_name,
                    array_to_json(array_agg(row_to_json(dc)))::JSONB as "filter_columns"
                    FROM admin_api.datatable_columns dc
                    WHERE dc.is_filterable IS TRUE
                    GROUP BY dc.table_name, dc.schema_name
                ) fc
                ON fc.table_name = dts.table_name
                AND fc.schema_name = dts.schema_name
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
                          NEW.custom_name,
                          NEW.order_index,
                          NEW.row_limit,
                          NEW.row_offset, 
                          NEW.schema_name, 
                          NEW.sort_column, 
                          NEW.sort_order,
                          NEW.table_name,
                          NEW.user_id
                          )
                          ON CONFLICT (user_id, schema_name, table_name)
                            DO UPDATE SET 
                                   row_offset=NEW.row_offset,
                                   sort_column=NEW.sort_column,
                                   sort_order=NEW.sort_order
                            WHERE admin.table_settings.user_id = NEW.user_id
                              AND admin.table_settings.table_name = NEW.table_name
                              AND admin.table_settings.schema_name = NEW.schema_name;
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
