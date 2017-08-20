from general.database.schema import Schema
from general.database.util import session_scope
from general.domains.auth.models import Users


class AdminApiSchema(Schema):
    name = 'admin_api'

    def __init__(self):
        super(AdminApiSchema, self).__init__()

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
