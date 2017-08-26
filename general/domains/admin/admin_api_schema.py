from general.database.schema import Schema
from general.database.util import session_scope

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

if __name__ == '__main__':
    admin_api_schema = AdminApiSchema()
    admin_api_schema.create_admin_api_views()
    admin_api_schema.grant_admin_privileges()
