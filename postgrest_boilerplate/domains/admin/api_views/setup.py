from .form_field_settings import create_form_field_settings_api_view
from .form_settings import (
    create_form_settings_api_view,
    create_form_settings_api_trigger
)
from .datatable import create_datatable_api_view, create_datatable_api_trigger
from .datatable_column_settings import (
    create_datatable_column_settings_api_view,
    create_datatable_column_settings_api_trigger
)
from .datatable_columns import (
    create_datatable_columns_api_view,
    create_datatable_columns_api_trigger
)
from .datatable_settings import (
    create_datatable_settings_api_view,
    create_datatable_settings_api_trigger
)
from .menubar import create_menubar_api_view
from .menubar_items import create_items_api_view


def create_admin_api_views():
    """
    Base API views introduce sensible defaults
        and limit access to the current user
    """
    create_datatable_settings_api_view()
    create_datatable_settings_api_trigger()

    create_datatable_column_settings_api_view()
    create_datatable_column_settings_api_trigger()

    create_form_settings_api_view()
    create_form_settings_api_trigger()

    create_form_field_settings_api_view()

    """
    Create API views that are specifically designed to be consumed by 
        frontend components
    """

    # The frontend joins these two views to provide a menubar with submenus
    create_items_api_view()
    create_menubar_api_view()

    # The frontend consumes the datatable endpoint to parameterize the
    # PrimeNG datatable component
    create_datatable_api_view()
    create_datatable_api_trigger()

    # The frontend consumes the datatable_columns endpoint to parameterize the
    # PrimeNG datatable component's columns
    create_datatable_columns_api_view()
    create_datatable_columns_api_trigger()

