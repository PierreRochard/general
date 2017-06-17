from sqlalchemy.exc import IntegrityError

from models import Submenus
from models.util import get_session


def insert_submenus(user):
    session = get_session()
    new_record = Submenus()
    new_record.user = user
    new_record.submenu_name = 'Settings'
    new_record.icon = 'fa-cogs'
    try:
        session.add(new_record)
        session.commit()
    except IntegrityError:
        session.rollback()


if __name__ == '__main__':
    insert_submenus('anon')
