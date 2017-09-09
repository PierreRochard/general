from sqlalchemy.orm.exc import NoResultFound

from general.database.session_scope import session_scope
from general.domains.admin.models import TableSettings
from general.domains.auth.models import Users


def insert_all_feature():
    menubar_view_names = ['menubar', 'items']
    schema_name = 'admin_api'
    with session_scope() as session:
        for user in session.query(Users).all():
            for menubar_view_name in menubar_view_names:
                try:
                    menubar_view_setting = (
                        session.query(TableSettings)
                            .filter(TableSettings.user_id == user.id)
                            .filter(
                            TableSettings.table_name == menubar_view_name)
                            .filter(TableSettings.schema_name == schema_name)
                            .one()
                    )
                except NoResultFound:
                    menubar_view_setting_data = {
                        'schema_name': schema_name,
                        'table_name':  menubar_view_name,
                        'user_id':     user.id
                    }
                    menubar_view_setting = TableSettings(
                        **menubar_view_setting_data)
                    session.add(menubar_view_setting)
                    session.commit()
                menubar_view_setting.is_visible = False
