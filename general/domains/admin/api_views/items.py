from general.database.util import session_scope


def create_items_view():
    """
    NB: we can't use the api.table_settings view in the items view as
    this will break our ability to join with submenu
    """
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.items CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin_api.items AS 
          SELECT coalesce(ts.custom_name, initcap(replace(t.table_name, '_', ' '))) as label,
                 coalesce(ts.icon, 'fa-table') AS icon,
                 coalesce(ts.id, auth.gen_random_uuid()) as id,
                 ts.submenu_id,
                 string_to_array('/' || t.table_name, ' ') AS "routerLink",
                 coalesce(ts.order_index, 0) AS order_index
          FROM admin.tables t
          LEFT OUTER JOIN admin.table_settings ts
              ON t.table_name = ts.table_name
          LEFT JOIN auth.users u
            ON ts.user_id = u.id
          WHERE u.role = current_user
            AND current_user != 'anon' AND ts.is_visible
          UNION
          SELECT coalesce(fs.custom_name, initcap(replace(f.form_name, '_', ' ')))::name as label,
                          CASE WHEN f.form_name = 'logout' 
                               THEN 'fa-sign-out' 
                               ELSE coalesce('fa-pencil-square-o', fs.icon)
                          END AS icon,
                          fs.id,
                          fs.submenu_id AS submenu_id,
                                 string_to_array('/rpc/' || f.form_name, ' ') 
                                    AS "routerLink",
                          fs.order_index
          FROM admin.forms f
          LEFT OUTER JOIN admin.form_settings fs
            ON f.form_name = fs.form_name
          LEFT JOIN auth.users u
            ON fs.user_id = u.id
          WHERE u.role = current_user
            AND (current_user != 'anon' AND f.form_name != 'login')
             OR (current_user  = 'anon' AND f.form_name  = 'login')
             AND fs.is_visible
          ORDER BY order_index ASC NULLS LAST, label ASC NULLS LAST;
          """)

if __name__ == '__main__':
    create_items_view()
