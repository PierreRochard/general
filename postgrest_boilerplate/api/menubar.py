"""
    params.set('select', 'label, icon, routerLink, items{label, icon, routerLink}');
    params.set('is_visible', 'is.true');
    return this.restClient.get('/menubar', params);
"""

from postgrest_boilerplate.models.util import session_scope


def create_api_items():
    with session_scope() as session:
        session.execute("""
        CREATE OR REPLACE VIEW api.items AS 
          SELECT ts.custom_name AS label,
                 ts.icon,
                 ts.id,
                 ts.submenu_id,
                 string_to_array('/' || ts.table_name, ' ') AS "routerLink",
                 ts.is_visible,
                 ts.order_index
          FROM api.table_settings ts
          WHERE current_user != 'anon'
          UNION
          SELECT coalesce(fs.custom_name, f.form_name) as label,
                          fs.icon,
                          fs.id,
                          fs.submenu_id AS submenu_id,
                                 string_to_array('/rpc/' || fs.form_name, ' ') 
                                    AS "routerLink",
                          fs.is_visible,
                          fs.order_index
          FROM admin.forms f
          LEFT OUTER JOIN admin.form_settings fs
            ON f.form_name = fs.form_name
            AND fs.user = current_user
          WHERE (current_user != 'anon' AND f.form_name != 'login')
             OR (current_user  = 'anon' AND f.form_name  = 'login')
          ORDER BY order_index ASC NULLS LAST, label ASC NULLS LAST;
          """)

        session.execute("""
        GRANT SELECT ON api.items TO anon;
        """)


def create_api_submenus():
    with session_scope() as session:
        session.execute("""
        CREATE OR REPLACE VIEW api.menubar AS
         SELECT s.id,
                s.submenu_name AS label,
                s.icon,
                string_to_array('', '') as "routerLink",
                s.is_visible,
                s.order_index
         FROM admin.submenus s
         WHERE s.user = current_user
           AND current_user != 'anon'
         UNION
         SELECT i.id,
                i.label,
                i.icon, 
                i."routerLink",
                i.is_visible,
                i.order_index
         FROM api.items i
         WHERE i.submenu_id IS NULL
         ORDER BY order_index ASC NULLS LAST, label ASC NULLS LAST;
        """)

        session.execute("""
        GRANT SELECT, UPDATE, INSERT ON api.menubar TO anon;
        """)
