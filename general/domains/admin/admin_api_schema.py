from general.database.schema import Schema
from general.database.util import session_scope
from general.domains.auth.models import Users


class AdminApiSchema(Schema):
    name = 'admin_api'

    def __init__(self):
        super(AdminApiSchema, self).__init__()


        # for user in session.query(Users).all():
        #     session.execute(f'GRANT SELECT ON api.menubar TO "{user.role}";')
        #     session.execute(f'GRANT SELECT ON api.items TO "{user.role}";')
        #     session.execute(f'GRANT SELECT, UPDATE ON api.datatable TO "{user.role}";')
        #     session.execute(f'GRANT SELECT, UPDATE ON api.datatable_columns TO "{user.role}";')

    def grant_admin_privileges(self):
        with session_scope() as session:
            privileges = {
                'ALL TABLES IN SCHEMA': {
                    'admin': {
                        'SELECT, UPDATE, INSERT': [u.role for u in
                                                   session.query(Users).all()]
                    }
                },
                'SCHEMA': {
                    'admin': {
                        'USAGE': [u.role for u in session.query(Users).all()]
                    }
                },
            }
        self.grant_privileges(self.name, privileges)
