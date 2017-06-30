import os
import sys

from models.util import session_scope
from scripts.insert_FormSettings import insert_form_settings
from scripts.insert_Submenus import insert_submenus
from scripts.insert_TableColumnSettings import insert_table_column_settings
from scripts.insert_TableSettings import insert_table_settings
from scripts.insert_User import insert_admin

sys.path.insert(0, '../')

from models import Base

from models.admin.datatable import create_datatable_function
from models.admin.datatable_columns import create_datatable_columns_function
from models.admin.form_settings import create_admin_forms_view
from models.admin.table_column_settings import create_admin_columns_view
from models.admin.tables import create_admin_tables_view

from models.auth.users import install_user_table_functions

from models.api.datatable import create_api_datatable_view
from models.api.datatable_columns import create_api_datatable_columns_view
from models.api.form_field_settings import create_api_form_field_settings
from models.api.form_settings import create_api_form_settings
from models.api.menubar import create_api_items, create_api_submenus
from models.api.table_column_settings import create_api_column_settings
from models.api.table_settings import create_api_table_settings


from scripts.setup_login import install_login_function
from scripts.setup_notifications import setup_table_notifications


# @compiles(DropTable, "postgresql")
# def _compile_drop_table(element, compiler, **kwargs):
#     return compiler.visit_drop_table(element) + " CASCADE"


def setup_database():
    with session_scope() as session:
        Base.metadata.create_all(session.connection())

    create_admin_tables_view()
    create_admin_columns_view()
    create_admin_forms_view()

    install_user_table_functions()
    install_login_function()

    for schema, table in [('api', 'messages')]:
        setup_table_notifications(schema, table)

    create_api_table_settings()
    create_api_column_settings()

    create_api_form_settings()
    create_api_form_field_settings()
    create_api_items()
    create_api_submenus()
    create_api_datatable_view()
    create_datatable_function()
    create_api_datatable_columns_view()
    create_datatable_columns_function()

    with session_scope() as session:
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
