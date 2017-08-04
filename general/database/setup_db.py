from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import DropTable

from general.database.util import session_scope, Base

from general.domains.admin.api_views.setup import (
    create_admin_api_views
)
from general.domains.admin.grant_privileges.all_users import \
    grant_admin_schema_privileges_to_users
from general.domains.admin.materialized_views.setup import (
    create_admin_materialized_views
)
from general.domains.auth.api_functions.setup import (
    create_auth_api_functions
)
from general.domains.auth.functions.setup import (
    create_auth_functions
)
from general.domains.auth.grant_privileges.all_users import \
    grant_privileges_to_users
from general.domains.auth.models.setup_triggers import (
    create_auth_table_triggers
)
from general.domains.auth.grant_privileges.all_users import (
    grant_privileges_to_anon
)
from general.domains.auth.types.jwt_token import (
    create_type_auth_jwt_token
)

# Necessary for models to register with Base
import general.domains.admin.models
import general.domains.auth.models
import general.domains.messaging.models


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def setup_database():
    with session_scope() as session:
        Base.metadata.drop_all(session.connection())
        Base.metadata.create_all(session.connection())

    create_admin_materialized_views()
    create_admin_api_views()

    create_type_auth_jwt_token()
    create_auth_functions()
    create_auth_api_functions()
    create_auth_table_triggers()
    grant_privileges_to_anon()
    grant_privileges_to_users()
    grant_admin_schema_privileges_to_users()


if __name__ == '__main__':
    setup_database()
