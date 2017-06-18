import os
import sys

from scripts.insert_FormSettings import insert_form_settings
from scripts.insert_Submenus import insert_submenus
from scripts.insert_TableColumnSettings import insert_table_column_settings
from scripts.insert_TableSettings import insert_table_settings
from scripts.insert_User import insert_admin

sys.path.insert(0, '../')

from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import DropTable

from models import (Base,
                    create_admin_tables_view,
                    create_admin_columns_view,
                    create_admin_forms_view,
                    create_api_column_settings, create_api_table_settings,
                    create_api_form_settings, create_api_submenus,
                    create_api_menubar_views, create_api_form_field_settings)
from scripts import get_pg_url
from scripts.setup_login import install_login_function
from scripts.setup_users_table import install_user_table_functions
from scripts.setup_notifications import setup_table_notifications


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def setup_database():
    engine = create_engine(get_pg_url(), echo=False)
    session = scoped_session(sessionmaker(bind=engine, autocommit=True))()
    session.connection().connection.set_isolation_level(0)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    create_admin_tables_view(session)
    create_admin_columns_view(session)
    create_admin_forms_view(session)

    install_user_table_functions(session)
    install_login_function(session)

    for schema, table in [('api', 'messages')]:
        setup_table_notifications(session, schema, table)

    create_api_table_settings(session)
    create_api_column_settings(session)

    create_api_form_settings(session)
    create_api_form_field_settings(session)
    create_api_menubar_views(session)
    create_api_submenus(session)

    session.execute("""
        REFRESH MATERIALIZED VIEW admin.tables;
        REFRESH MATERIALIZED VIEW admin.columns;
        REFRESH MATERIALIZED VIEW admin.forms;
        """)

    insert_submenus('anon')
    insert_form_settings('anon')
    insert_table_settings('anon')

    insert_admin()

    insert_submenus(os.environ['REST_USER'])
    insert_form_settings(os.environ['REST_USER'])
    insert_table_settings(os.environ['REST_USER'])
    insert_table_column_settings(os.environ['REST_USER'])


if __name__ == '__main__':
    setup_database()
