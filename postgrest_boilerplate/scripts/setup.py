import os

from postgrest_boilerplate.models.util import session_scope
from postgrest_boilerplate.scripts.admin import (
    insert_submenus,
    insert_form_settings,
    insert_table_settings,
    insert_table_column_settings
)

from postgrest_boilerplate.models import Base
from postgrest_boilerplate.models.admin import (
    create_datatable_function,
    create_datatable_columns_function,
    create_admin_forms_view,
    create_admin_columns_view,
    create_admin_tables_view
)

from postgrest_boilerplate.models.auth.users import install_user_table_functions

from postgrest_boilerplate.api import (
    create_api_datatable_view,
    create_api_datatable_columns_view,
    create_api_form_field_settings,
    create_api_form_settings,
    create_api_items,
    create_api_submenus,
    create_api_column_settings,
    create_api_table_settings
)

from postgrest_boilerplate.scripts.auth import (
    install_login_function,
    insert_admin
)
from postgrest_boilerplate.scripts.api import setup_table_notifications


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
