from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import DropTable

from general.database.base import Base
from general.database.session_scope import session_scope


# Necessary for models to register with Base
import general.domains.admin.models
import general.domains.auth.models


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def reset_database():
    with session_scope() as session:
        Base.metadata.drop_all(session.connection())
        Base.metadata.create_all(session.connection())

if __name__ == '__main__':
    reset_database()
