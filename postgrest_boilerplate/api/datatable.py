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
          CREATE TRIGGER datatable_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON api.datatable
          FOR EACH ROW
          EXECUTE PROCEDURE admin.datatable_function();
        """)
