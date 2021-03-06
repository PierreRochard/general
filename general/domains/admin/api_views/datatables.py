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
                       dts.context_menu_items,
                       map.mapper_settings
                FROM admin.default_datatable_settings dts
                LEFT OUTER JOIN (
                  SELECT
                    mq.table_settings_id,
                    row_to_json(mq)::JSONB AS "mapper_settings"
                    FROM 
                    (
                    SELECT
                      ms.table_settings_id,
                      row_to_json(fcdc) AS filter_column,
                      row_to_json(mcdc) AS mapping_column,
                      row_to_json(smcdc) AS saved_keyword_column,
                      row_to_json(skdc) AS saved_mapping_column
                    FROM ADMIN.mapper_settings MS
                    LEFT JOIN ADMIN.default_datatable_column_settings fcdc
                    ON fcdc.id = MS.filter_column_settings_id
                    LEFT JOIN ADMIN.default_datatable_column_settings mcdc
                    ON mcdc.id = MS.mapping_column_settings_id
                    LEFT JOIN ADMIN.default_datatable_column_settings smcdc
                    ON smcdc.id = MS.saved_mapping_column_settings_id
                    LEFT JOIN ADMIN.default_datatable_column_settings skdc
                    ON skdc.id = MS.saved_keyword_column_settings_id
                    ) mq
                ) map
                ON dts.id = map.table_settings_id
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
