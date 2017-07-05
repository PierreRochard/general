from postgrest_boilerplate.models.util import session_scope


def create_api_datatable_view():
    with session_scope() as session:
        session.execute("""
          CREATE OR REPLACE VIEW api.datatable AS
          
            SELECT (row_number() OVER())::INT id, *
            FROM (
                SELECT ts.table_name AS name, 
                       ts.custom_name AS header,
                       ts.row_limit AS "limit",
                       ts.row_offset AS "offset",
                       ts.sort_column,
                       ts.sort_order
                FROM api.table_settings ts
            ) sub;
        """)

        session.execute("""
         GRANT SELECT ON api.datatable TO anon;
        """)

        session.execute("""
          DROP TRIGGER IF EXISTS datatable_trigger ON api.datatable;
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
          CREATE TRIGGER datatable_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON api.datatable
          FOR EACH ROW
          EXECUTE PROCEDURE admin.datatable_function();
        """)
