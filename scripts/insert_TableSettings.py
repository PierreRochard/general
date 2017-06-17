from models.util import get_session
from models import Submenus, TableSettings


def insert_table_settings(user):
    session = get_session()
    for table_name, in session.execute('SELECT table_name FROM admin.tables'):
        submenu_id = None
        if table_name.endswith('settings'):
            submenu_name = 'Settings'
            submenu_id = (session.query(Submenus.id)
                          .filter(Submenus.submenu_name == submenu_name)
                          .filter(Submenus.user == user)
                          .scalar())

        new_record_data = {
            'user': user,
            'table_name': table_name,
            'custom_name': table_name.replace('_', ' ').title(),
            'icon': 'fa-table',
            'submenu_id': str(submenu_id) if submenu_id else None
        }
        new_record = TableSettings(**new_record_data)
        session.add(new_record)
        session.commit()


if __name__ == '__main__':
    insert_table_settings('anon')
