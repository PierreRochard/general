from postgrest_boilerplate.database.util import session_scope


def create_items_api_view():
    """
    NB: we can't use the api.table_settings view in the items view as
    this will break our ability to join with submenu
    """
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS api.items CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW api.items AS 
          SELECT coalesce(ts.custom_name, initcap(replace(t.table_name, '_', ' '))) as label,
                 coalesce(ts.icon, 'fa-table') AS icon,
                 coalesce(ts.id, auth.gen_random_uuid()) as id,
                 ts.submenu_id,
                 string_to_array('/' || t.table_name, ' ') AS "routerLink",
                 coalesce(ts.order_index, 0) AS order_index
          FROM admin.tables t
          LEFT OUTER JOIN admin.table_settings ts
              ON t.table_name = ts.table_name
              AND ts.user = current_user
          WHERE current_user != 'anon' AND ts.is_visible
          UNION
          SELECT coalesce(fs.custom_name, f.form_name) as label,
                          fs.icon,
                          fs.id,
                          fs.submenu_id AS submenu_id,
                                 string_to_array('/rpc/' || fs.form_name, ' ') 
                                    AS "routerLink",
                          fs.order_index
          FROM admin.forms f
          LEFT OUTER JOIN admin.form_settings fs
            ON f.form_name = fs.form_name
            AND fs.user = current_user
          WHERE (current_user != 'anon' AND f.form_name != 'login')
             OR (current_user  = 'anon' AND f.form_name  = 'login')
             AND fs.is_visible
          ORDER BY order_index ASC NULLS LAST, label ASC NULLS LAST;
          """)

        session.execute("""
        GRANT SELECT ON api.items TO anon;
        """)

if __name__ == '__main__':
    create_items_api_view()
