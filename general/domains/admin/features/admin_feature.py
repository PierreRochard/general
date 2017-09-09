from sqlalchemy.orm.exc import NoResultFound

from general.database.session_scope import session_scope
from general.domains.admin.models.feature_sets import FeatureSets
from general.domains.admin.models.feature_sets_users import \
    FeatureSetsUsers
from general.domains.admin.models.submenus import Submenus
from general.domains.admin.models.table_settings import TableSettings


def insert_admin_feature():
    with session_scope() as session:
        feature_sets_users = (
            session
                .query(FeatureSetsUsers)
                .filter(FeatureSets.name == 'admin')
                .all()
        )
        for feature_set_user in feature_sets_users:
            schema_name = 'admin_api'
            user_id = feature_set_user.user_id
            submenu_name = 'Settings'
            try:
                submenu = (
                    session.query(Submenus)
                        .filter(Submenus.submenu_name == submenu_name)
                        .filter(Submenus.user_id == user_id)
                        .one()
                )
            except NoResultFound:
                submenu = Submenus()
                submenu.user_id = feature_set_user.user_id
                submenu.submenu_name = submenu_name
                submenu.icon = 'fa-cogs'
                session.add(submenu)
                session.commit()

            api_view_names = ['datatable_columns',
                              'datatables',
                              'form_fields',
                              'forms']
            for api_view_name in api_view_names:
                try:
                    menubar_view_setting = (
                        session.query(TableSettings)
                            .filter(TableSettings.user_id == user_id)
                            .filter(TableSettings.table_name == api_view_name)
                            .filter(TableSettings.schema_name == schema_name)
                            .one()
                    )
                except NoResultFound:
                    menubar_view_setting_data = {
                        'schema_name': schema_name,
                        'table_name':  api_view_name,
                        'user_id':     user_id
                    }
                    menubar_view_setting = TableSettings(
                        **menubar_view_setting_data)
                    session.add(menubar_view_setting)
                    session.commit()
                menubar_view_setting.submenu_id = submenu.id

            menubar_view_names = ['menubar', 'items']
            for menubar_view_name in menubar_view_names:
                try:
                    menubar_view_setting = (
                        session.query(TableSettings)
                            .filter(TableSettings.user_id == user_id)
                            .filter(
                            TableSettings.table_name == menubar_view_name)
                            .filter(TableSettings.schema_name == schema_name)
                            .one()
                    )
                except NoResultFound:
                    menubar_view_setting_data = {
                        'schema_name': schema_name,
                        'table_name':  menubar_view_name,
                        'user_id':     user_id
                    }
                    menubar_view_setting = TableSettings(
                        **menubar_view_setting_data)
                    session.add(menubar_view_setting)
                    session.commit()
                menubar_view_setting.is_visible = False
