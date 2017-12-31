from sqlalchemy.orm.exc import NoResultFound

from general.database.session_scope import session_scope
from general.domains.admin.models.feature_sets import FeatureSets
from general.domains.admin.models.feature_sets_users import \
    FeatureSetsUsers
from general.domains.admin.models.table_settings import TableSettings
from general.domains.auth.models import Users


def insert_user_feature():
    """
    The user feature set is the opposite of the admin feature set.
    Hide the admin tables.
    """
    schema_name = 'admin'
    api_view_names = ['datatable_columns',
                      'datatables',
                      'form_fields',
                      'forms',
                      'home']
    with session_scope() as session:
        users = (
            session
                .query(Users)
                .outerjoin(FeatureSetsUsers,
                           FeatureSetsUsers.user_id == Users.id)
                .outerjoin(FeatureSets,
                           FeatureSetsUsers.feature_set_id == FeatureSets.id)
                .filter(FeatureSets.name.is_(None))
                .all()
        )
        user_ids = [user.id for user in users]
        for user in users:
            for api_view_name in api_view_names:
                try:
                    menubar_view_setting = (
                        session.query(TableSettings)
                            .filter(TableSettings.user_id == user.id)
                            .filter(TableSettings.table_name == api_view_name)
                            .filter(TableSettings.schema_name == schema_name)
                            .one()
                    )
                except NoResultFound:
                    menubar_view_setting_data = {
                        'schema_name': schema_name,
                        'table_name':  api_view_name,
                        'user_id':     user.id
                    }
                    menubar_view_setting = TableSettings(
                        **menubar_view_setting_data)
                    session.add(menubar_view_setting)
                    session.commit()
                menubar_view_setting.is_visible = False
