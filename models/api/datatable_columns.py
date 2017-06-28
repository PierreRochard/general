from models.util import session_scope


def create_api_datatable_columns_view():
    with session_scope() as session:
        session.execute("""
          CREATE OR REPLACE VIEW api.datatable_columns AS
            SELECT c.table_name, 
                   c.column_name as value, 
                   coalesce(cs.custom_name, c.column_name) as label,
                   cs.filter_match_mode,
                   cs.filter_value,
                   cs.is_filterable,
                   cs.is_sortable,
                   cs.is_visible,
                   cs.order_index
            FROM admin.columns c
              LEFT OUTER JOIN admin.table_column_settings cs
                ON c.table_name = cs.table_name
                   AND c.column_name = cs.column_name
                   AND cs.user = current_user
          ORDER BY order_index ASC NULLS LAST;
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
