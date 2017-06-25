from models.util import session_scope


def create_api_datatable_view():
    with session_scope() as session:
        session.execute("""
          CREATE OR REPLACE VIEW api.datatable AS
            SELECT t.table_name, 
                   coalesce(ts.custom_name, t.table_name) as header,
                   ts.row_limit
            FROM admin.tables t
              LEFT OUTER JOIN admin.table_settings ts
                ON t.table_name = ts.table_name
                   AND ts.user = current_user;
        """)

        session.execute("""
         GRANT SELECT ON api.datatable TO anon;
        """)
