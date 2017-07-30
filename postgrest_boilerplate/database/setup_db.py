from postgrest_boilerplate.database.util import session_scope, Base

from postgrest_boilerplate.domains.admin.api_views.setup import (
    create_admin_api_views
)
from postgrest_boilerplate.domains.admin.materialized_views.setup import (
    create_admin_materialized_views
)
from postgrest_boilerplate.domains.auth.api_functions.setup import (
    create_auth_api_functions
)
from postgrest_boilerplate.domains.auth.functions.setup import (
    create_auth_functions
)
from postgrest_boilerplate.domains.auth.models.setup_triggers import (
    create_auth_table_triggers
)
from postgrest_boilerplate.domains.auth.grant_privileges.users_table import (
    grant_privileges_to_anon
)
from postgrest_boilerplate.domains.auth.types.jwt_token import (
    create_type_auth_jwt_token
)

# Necessary for models to register with Base
import postgrest_boilerplate.domains.admin.models
import postgrest_boilerplate.domains.auth.models
import postgrest_boilerplate.domains.messaging.models


def setup_database():
    with session_scope() as session:
        Base.metadata.create_all(session.connection())

    create_admin_materialized_views()
    create_admin_api_views()

    create_type_auth_jwt_token()
    create_auth_functions()
    create_auth_api_functions()
    create_auth_table_triggers()
    grant_privileges_to_anon()


if __name__ == '__main__':
    setup_database()
