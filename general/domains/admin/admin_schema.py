from general.database.schema import Schema
from general.database.util import session_scope
from general.domains.auth.models import Users


class AdminSchema(Schema):
    name = 'auth'

    def __init__(self):
        super(AdminSchema, self).__init__()

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
