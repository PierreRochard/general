from postgrest_boilerplate.database.util import session_scope, Base


from postgrest_boilerplate.domains.admin.api_views.setup import (
    create_admin_api_views
)
from postgrest_boilerplate.domains.admin.materialized_views.setup import (
    create_admin_materialized_views
)


# Necessary for models to register with Base
import postgrest_boilerplate.domains.admin.models


def setup_database():
    with session_scope() as session:
        Base.metadata.create_all(session.connection())

    create_admin_materialized_views()

    create_admin_api_views()


if __name__ == '__main__':
    setup_database()
