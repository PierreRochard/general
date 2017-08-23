from general.database.schema import Schema
from general.database.util import session_scope

from general.domains.auth.models import Users



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
        create_items_api_view()
        create_menubar_api_view()
    
        # The frontend consumes the datatable endpoint to parameterize the
        # PrimeNG datatable component
        create_datatable_api_view()
        create_datatable_api_trigger()
    
        # The frontend consumes the datatable_columns endpoint to parameterize the
        # PrimeNG datatable component's columns
        create_datatable_columns_api_view()
        create_datatable_columns_api_trigger()

    def grant_admin_privileges(self):
        with session_scope() as session:
            privileges = {
                'ALL TABLES IN SCHEMA': {
                    'admin_api': {
                        'SELECT, UPDATE, INSERT': [u.role for u in
                                                   session.query(Users).all()]
                    }
                },
                'SCHEMA':               {
                    'admin_api': {
                        'USAGE': [u.role for u in session.query(Users).all()]
                                     .append('anon')
                    }
                },
                'VIEW':                 {
                    'menubar':   {
                        'SELECT': [u.role for u in session.query(Users).all()]
                                      .append('anon')
                    },
                    'items':     {
                        'SELECT': [u.role for u in session.query(Users).all()]
                                      .append('anon')
                    },
                    'datatable': {
                        'SELECT, UPDATE': [u.role for u in
                                           session.query(Users).all()]
                    },
                    'datatable_columns': {
                        'SELECT, UPDATE': [u.role for u in
                                           session.query(Users).all()]
                    }
                }
            }
        self.grant_privileges(self.name, privileges)
