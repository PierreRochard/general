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
        from general.domains.admin.models.feature_sets_users import FeatureSetsUsers
        from general.domains.admin.models.submenus import Submenus
        with session_scope() as session:
            users = (
                session
                    .query(FeatureSetsUsers)
                    .filter(FeatureSets.name == 'admin')
                    .all()
            )
            for user in users:
                new_submenu = Submenus()
                new_submenu.user_id = user.id
                new_submenu.submenu_name = 'Settings'
                new_submenu.icon = 'fa-cogs'
                with session_scope(raise_integrity_error=False) as inner_session:
                    inner_session.add(new_submenu)

    def grant_admin_privileges(self):
        from general.domains.auth.models import Users
        with session_scope() as session:
            privileges = {
                'SCHEMA':               {
                    'admin_api': {
                        'USAGE': [u.role for u in session.query(Users).all()]
                    }
                },
                'VIEW':                 {
                    'menubar':   {
                        'SELECT': [u.role for u in session.query(Users).all()]
                    },
                    'items':     {
                        'SELECT': [u.role for u in session.query(Users).all()]
                    },
                    'forms':     {
                        'SELECT': [u.role for u in session.query(Users).all()],
                        'UPDATE': [u.role for u in session.query(Users).all()
                                   if u.role != 'anon']
                    },
                    'form_fields':     {
                        'SELECT': [u.role for u in session.query(Users).all()],
                        'UPDATE': [u.role for u in session.query(Users).all()
                                   if u.role != 'anon']
                    },
                    'datatables': {
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
        self.create_admin_api_views()
        self.insert_feature_records()
        self.grant_admin_privileges()
