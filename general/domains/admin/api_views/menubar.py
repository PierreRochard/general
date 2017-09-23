
"""
Frontend usage:
params.set('select', 'label, icon, routerLink, items');
return this.restClient.get('/menubar', params);
"""

from general.database.session_scope import session_scope


def create_menubar_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.menubar CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin_api.menubar AS
         SELECT m."label",
                m.icon,
                m."routerLink",
                m.items
         FROM admin.menubar m
         WHERE m."user" = current_user;
        """)

if __name__ == '__main__':
    create_menubar_view()
