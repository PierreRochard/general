from postgrest_boilerplate.models.util import session_scope


def create_api_datatable_columns_view():
    with session_scope() as session:
        session.execute("""
          CREATE OR REPLACE VIEW api.datatable_columns AS
            SELECT tcs.table_name, 
                   tcs.column_name as value, 
                   tcs.custom_name as label,
                   tcs.filter_match_mode,
                   tcs.filter_value,
                   tcs.is_filterable,
                   tcs.is_sortable,
                   tcs.is_visible,
                   tcs.order_index
            FROM api.table_column_settings tcs
          ORDER BY order_index ASC;
        """)

        session.execute("""
         GRANT SELECT ON api.datatable_columns TO anon;
        """)

        session.execute("""
          DROP TRIGGER IF EXISTS datatable_columns_trigger ON api.datatable_columns;
        """)

        session.execute("""
          CREATE TRIGGER datatable_columns_trigger
          INSTEAD OF INSERT OR UPDATE OR DELETE
          ON api.datatable_columns
          FOR EACH ROW
          EXECUTE PROCEDURE admin.datatable_columns_function();
        """)
