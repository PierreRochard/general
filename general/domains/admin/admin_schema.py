import os

from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm.exc import NoResultFound

from general.database.base import Base
from general.database.schema import Schema
from general.database.session_scope import session_scope

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
    create_default_form_settings_view,
    create_default_home_settings_view,
    create_menubar_view,
    create_submenu_items_view
)


class AdminSchema(Schema):

    def __init__(self):
        super(AdminSchema, self).__init__(name='admin')

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
        create_default_home_settings_view()
        create_submenu_items_view()
        create_menubar_view()

    @staticmethod
    def insert_anon():
        from general.domains.auth.models import Users
        with session_scope() as session:
            try:
                session.execute("""
                CREATE ROLE anon noinherit;
                """)
            except ProgrammingError:
                pass
            try:
                user = (
                    session.query(Users)
                        .filter(Users.role == 'anon')
                        .one()
                )
            except NoResultFound:
                user = Users()
                user.role = 'anon'
                user.active = True
                session.add(user)

    @staticmethod
    def insert_admin_feature():
        from general.domains.admin.models.feature_sets import FeatureSets
        from general.domains.admin.models.feature_sets_users import FeatureSetsUsers
        from general.domains.auth.models.users import Users
        with session_scope(raise_integrity_error=False) as session:
            new_feature_set = FeatureSets()
            new_feature_set.name = 'admin'
            session.add(new_feature_set)

        with session_scope(raise_integrity_error=False) as session:
            admin_feature_set = (
                session.query(FeatureSets)
                    .filter(FeatureSets.name == 'admin')
                    .one()
            )
            user_role = os.environ['PGUSER']
            try:
                user = (
                    session.query(Users)
                        .filter(Users.role == user_role)
                        .one()
                )
            except NoResultFound:
                user = Users()
                user.role = user_role
                user.active = True
                session.add(user)
                session.commit()
            new_feature_sets_users = FeatureSetsUsers()
            new_feature_sets_users.user_id = user.id
            new_feature_sets_users.feature_set_id = admin_feature_set.id
            session.add(new_feature_sets_users)

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
        self.create_schema()
        self.create_tables()
        self.create_materialized_views()
        self.create_admin_views()
        self.insert_anon()
        self.insert_admin_feature()
        self.grant_admin_privileges()
