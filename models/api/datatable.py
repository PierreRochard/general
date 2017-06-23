from models.util import session_scope


def create_api_datatable_view():
    with session_scope() as session:
        session.execute("""
          CREATE OR REPLACE VIEW api.datatable AS
            SELECT c.table_name, 
                   c.column_name as field, 
                   coalesce(cs.custom_name, c.column_name) as header,
                   cs.order_index
            FROM admin.columns c
              LEFT OUTER JOIN admin.table_column_settings cs
                ON c.table_name = cs.table_name
                   AND c.column_name = cs.column_name
                   AND cs.user = current_user
          ORDER BY order_index ASC NULLS LAST, field ASC NULLS LAST;
        """)

