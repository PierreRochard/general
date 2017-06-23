from sqlalchemy.exc import IntegrityError

from models.util import get_session
from models import Submenus, FormSettings


def insert_form_settings(user):
    session = get_session()

    for form_name, in session.execute('SELECT form_name FROM admin.forms'):
        new_record_data = {
            'user': user,
            'form_name': form_name,
            'custom_name': form_name.replace('_', ' ').title(),
            'icon': 'fa-pencil-square-o',
            'submenu_id': None,
            'order_index': 10,
        }
        new_record = FormSettings(**new_record_data)
        try:
            session.add(new_record)
            session.commit()
        except IntegrityError:
            session.rollback()


if __name__ == '__main__':
    insert_form_settings('anon')
