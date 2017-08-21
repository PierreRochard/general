from general.database.schema import Schema
from general.database.util import session_scope
from .materialized_views import (
    create_columns_materialized_view,
    create_fields_intermediate_view,
    create_fields_materialized_view,
    create_forms_materialized_view,
    create_materialized_views_refresh_trigger,
    create_tables_materialized_view
)
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

    @staticmethod
    def create_materialized_views(self):
        create_columns_materialized_view()
        create_fields_intermediate_view()
        create_fields_materialized_view()
        create_forms_materialized_view()
        create_tables_materialized_view()
        create_materialized_views_refresh_trigger()
