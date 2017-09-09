from sqlalchemy.orm.exc import NoResultFound

from general.database.session_scope import session_scope
from general.domains.admin.models.feature_sets import FeatureSets
from general.domains.admin.models.feature_sets_users import \
    FeatureSetsUsers
from general.domains.admin.models.submenus import Submenus
from general.domains.admin.models.table_settings import TableSettings
from general.domains.auth.models import Users


def insert_admin_feature():
    schema_name = 'admin_api'
    submenu_name = 'Settings'
    submenu_icon = 'fa-cogs'
    api_view_names = ['datatable_columns',
                      'datatables',
                      'form_fields',
                      'forms']
    
    with session_scope() as session:
        users = (
            session
                .query(Users)
                .outerjoin(FeatureSetsUsers,
                           FeatureSetsUsers.user_id == Users.id)
                .outerjoin(FeatureSets,
                           FeatureSetsUsers.feature_set_id == FeatureSets.id)
                .filter(FeatureSets.name == 'admin')
                .all()
        )
        for user in users:
            try:
                submenu = (
                    session.query(Submenus)
                        .filter(Submenus.submenu_name == submenu_name)
                        .filter(Submenus.user_id == user.id)
                        .one()
                )
            except NoResultFound:
                submenu = Submenus()
                submenu.user_id = user.id
                submenu.submenu_name = submenu_name
                session.add(submenu)
                session.commit()
            submenu.icon = submenu_icon

            for api_view_name in api_view_names:
                try:
                    menubar_view_setting = (
                        session.query(TableSettings)
                            .filter(TableSettings.user_id == user.id)
                            .filter(TableSettings.table_name == api_view_name)
                            .filter(TableSettings.schema_name == schema_name)
                            .one()
                    )
                except NoResultFound:
                    menubar_view_setting_data = {
                        'schema_name': schema_name,
                        'table_name':  api_view_name,
                        'user_id':     user.id
                    }
                    menubar_view_setting = TableSettings(
                        **menubar_view_setting_data)
                    session.add(menubar_view_setting)
                    session.commit()
                menubar_view_setting.submenu_id = submenu.id
