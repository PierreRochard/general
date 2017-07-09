from postgrest_boilerplate.database.util import session_scope, Base


from postgrest_boilerplate.domains.admin.api_views.setup import (
    create_admin_api_views
)

# @compiles(DropTable, "postgresql")
# def _compile_drop_table(element, compiler, **kwargs):
#     return compiler.visit_drop_table(element) + " CASCADE"


def setup_database():
    with session_scope() as session:
        Base.metadata.create_all(session.connection())

    with session_scope() as session:
        session.execute("""
                REFRESH MATERIALIZED VIEW admin.tables;
                REFRESH MATERIALIZED VIEW admin.columns;
                REFRESH MATERIALIZED VIEW admin.forms;
                """)

    create_admin_api_views()


if __name__ == '__main__':
    setup_database()
