from .refresh_trigger import create_materialized_views_refresh_trigger
from .columns import create_columns_materialized_view
from .forms import create_forms_materialized_view
from .tables import create_tables_materialized_view


def create_admin_materialized_views():
    """
    Materialized views which select from PostgreSQL system tables
        to provide the tables and procedures/functions being exposed
         in the API schema
    """

    create_columns_materialized_view()
    create_forms_materialized_view()
    create_tables_materialized_view()

    # Ensures that DDL commands trigger a materialized view refresh
    create_materialized_views_refresh_trigger()
