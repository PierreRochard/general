from sqlalchemy.orm.exc import NoResultFound

from general.database.schema import Schema
from general.database.session_scope import session_scope

from general.domains.admin.api_views import (
    create_datatable_columns_trigger,
    create_datatable_columns_view,
    create_datatables_trigger,
    create_datatables_view,
    create_form_fields_view,
    create_forms_view,
    create_items_view,
    create_menubar_view
)
from general.domains.admin.models import TableSettings


class AdminApiSchema(Schema):
    def __init__(self):
        super(AdminApiSchema, self).__init__(name='admin_api')

    @staticmethod
    def create_admin_api_views():
        """
        Create API views that are specifically designed to be consumed by 
            frontend components
        """

        # The frontend joins these two views to provide a menubar with submenus
        create_items_view()
        create_menubar_view()

        # The frontend consumes the datatable endpoint to parameterize the
        # PrimeNG datatable component
        create_datatables_view()
        create_datatables_trigger()

        # The frontend consumes the datatable_columns endpoint to parameterize the
        # PrimeNG datatable component's columns
        create_datatable_columns_view()
        create_datatable_columns_trigger()

        create_forms_view()
        create_form_fields_view()

    @staticmethod
    def insert_feature_records():
        from general.domains.auth.models.users import Users
        from general.domains.admin.models.feature_sets import FeatureSets
        from general.domains.admin.models.feature_sets_users import \
            FeatureSetsUsers
        from general.domains.admin.models.submenus import Submenus
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
                        api_view_setting = (
                            session.query(TableSettings)
                            .filter(TableSettings.user_id == user_id)
                            .filter(TableSettings.table_name == api_view_name)
                            .filter(TableSettings.schema_name == schema_name)
                            .one()
                        )
                    except NoResultFound:
                        api_view_setting_data = {
                                'schema_name': schema_name,
                                'table_name':  api_view_name,
                                'user_id':     user_id
                            }
                        api_view_setting = TableSettings(**api_view_setting_data)
                        session.add(api_view_setting)
                        session.commit()
                    api_view_setting.submenu_id = submenu.id

    def grant_admin_privileges(self):
        from general.domains.auth.models import Users
        with session_scope() as session:
            privileges = {
                'SCHEMA': {
                    'admin_api': {
                        'USAGE': [u.role for u in session.query(Users).all()]
                    }
                },
                'VIEW':   {
                    'menubar':           {
                        'SELECT': [u.role for u in session.query(Users).all()]
                    },
                    'items':             {
                        'SELECT': [u.role for u in session.query(Users).all()]
                    },
                    'forms':             {
                        'SELECT': [u.role for u in session.query(Users).all()],
                        'UPDATE': [u.role for u in session.query(Users).all()
                                   if u.role != 'anon']
                    },
                    'form_fields':       {
                        'SELECT': [u.role for u in session.query(Users).all()],
                        'UPDATE': [u.role for u in session.query(Users).all()
                                   if u.role != 'anon']
                    },
                    'datatables':        {
                        'SELECT, UPDATE': [u.role for u in
                                           session.query(Users).all()
                                           if u.role != 'anon']
                    },
                    'datatable_columns': {
                        'SELECT, UPDATE': [u.role for u in
                                           session.query(Users).all()
                                           if u.role != 'anon']
                    }
                }
            }
        self.grant_privileges(self.name, privileges)

    def setup(self):
        self.create_schema()
        self.create_admin_api_views()
        self.insert_feature_records()
        self.grant_admin_privileges()
