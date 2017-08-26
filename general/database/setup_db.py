from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import DropTable

from general.database.util import session_scope, Base


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
