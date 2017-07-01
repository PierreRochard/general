from models import Submenus

from postgrest_boilerplate.models.util import session_scope


def insert_submenus(user):
    new_record = Submenus()
    new_record.user = user
    new_record.submenu_name = 'Settings'
    new_record.icon = 'fa-cogs'
    new_record.order_index = 2
    with session_scope() as session:
        session.add(new_record)


if __name__ == '__main__':
    insert_submenus('anon')
