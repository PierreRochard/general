from general.database.util import session_scope


def create_menubar_api_view():
    """
    Frontend usage:
    params.set('select', 'label, icon, routerLink, items{label, icon, routerLink}');
    params.set('is_visible', 'is.true');
    return this.restClient.get('/menubar', params);
    """
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.menubar CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin_api.menubar AS
         SELECT s.id,
                s.submenu_name AS label,
                s.icon,
                string_to_array('', '') as "routerLink",
                s.order_index
         FROM admin.submenus s
         LEFT JOIN auth.users u 
          ON u.id = s.user_id
         WHERE u.role = current_user
           AND s.is_visible
           AND current_user != 'anon'
         UNION
         SELECT i.id,
                i.label,
                i.icon, 
                i."routerLink",
                i.order_index
         FROM admin_api.items i
         WHERE i.submenu_id IS NULL
         ORDER BY order_index ASC NULLS LAST, label ASC NULLS LAST;
        """)

if __name__ == '__main__':
    create_menubar_api_view()
