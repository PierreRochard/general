from pprint import pformat

from models.util import get_session
from models import Submenus, FormSettings


def insert_form_settings(user):
    session = get_session()
    submenu_id = (session.query(Submenus.id)
                  .filter(Submenus.submenu_name == 'Settings')
                  .filter(Submenus.user == user)
                  .scalar())
    for form_name, in session.execute('SELECT form_name FROM admin.forms'):
        print(form_name)
        new_record_data = {
            'user': user,
            'form_name': form_name,
            'custom_name': form_name.replace('_', ' ').title(),
            'icon': 'fa-pencil-square-o',
            'submenu_id': str(submenu_id)
        }
        print(pformat(new_record_data))
        new_record = FormSettings(**new_record_data)
        session.add(new_record)
        session.commit()


if __name__ == '__main__':
    insert_form_settings('anon')
