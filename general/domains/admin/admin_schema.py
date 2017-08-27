from general.database.schema import Schema
from general.database.util import session_scope, Base

from general.domains.admin.materialized_views import (
    create_form_fields_materialized_view,
    create_forms_materialized_view,
    create_materialized_views_refresh_trigger,
    create_schemas_materialized_view,
    create_table_columns_materialized_view,
    create_tables_materialized_view
)
from general.domains.admin.views import (
    create_default_datatable_column_settings_view,
    create_default_datatable_settings_view,
    create_default_form_field_settings_view,
    create_default_form_settings_view
)


class AdminSchema(Schema):

    def __init__(self):
        super(AdminSchema, self).__init__(name='auth')

    @staticmethod
    def create_tables():
        import general.domains.admin.models
        with session_scope() as session:
            Base.metadata.create_all(session.connection())

    @staticmethod
    def create_materialized_views():
        """
        Materialized views that pull from system tables and a
            refresh trigger for to keep the data fresh
        """
        create_form_fields_materialized_view()
        create_forms_materialized_view()
        create_schemas_materialized_view()
        create_table_columns_materialized_view()
        create_tables_materialized_view()
        create_materialized_views_refresh_trigger()

    @staticmethod
    def create_admin_views():
        """
        Base views introduce sensible defaults
            and limit access to the current user
        """
        create_default_datatable_column_settings_view()
        create_default_datatable_settings_view()
        create_default_form_field_settings_view()
        create_default_form_settings_view()

    def grant_admin_privileges(self):
        from general.domains.auth.models import Users
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

    def setup(self):
        self.create_tables()
        self.create_materialized_views()
        self.create_admin_views()
        self.grant_admin_privileges()
