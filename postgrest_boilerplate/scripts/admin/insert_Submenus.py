from sqlalchemy.orm.exc import NoResultFound

from postgrest_boilerplate.models.admin import Submenus, TableSettings
from postgrest_boilerplate.models.auth import Users
from postgrest_boilerplate.models.util import session_scope


def insert_submenu(name: str, icon: str, order_index: int, items: list):

    with session_scope() as session:
        users = session.query(Users.role).all()
        users = [r[0] for r in users]
    users.append('anon')

    for user in users:
        insert_user_submenu(user=user,
                            name=name,
                            icon=icon,
                            order_index=order_index,
                            items=items)


def insert_user_submenu(user: str, name: str, icon: str, order_index: int,
                        items: list):
    submenu_name = name
    new_record = Submenus()
    new_record.user = user
    new_record.submenu_name = submenu_name
    new_record.icon = icon
    new_record.order_index = order_index
    with session_scope() as session:
        session.add(new_record)
    for item in items:
        with session_scope() as session:
            submenu_id = (
                session
                    .query(Submenus.id)
                    .filter(Submenus.submenu_name == submenu_name)
                    .filter(Submenus.user == user)
                    .scalar()
            )
            try:
                setting = (
                    session
                        .query(TableSettings)
                        .filter(TableSettings.table_name == item)
                        .filter(TableSettings.user == user)
                        .one()
                )
            except NoResultFound:
                setting = TableSettings()
                setting.user = user
                setting.table_name = item
                session.add(setting)
            setting.submenu_id = str(submenu_id)


if __name__ == '__main__':
    insert_submenu(name='Settings', icon='fa-cogs', order_index=3,
                   items=[])
