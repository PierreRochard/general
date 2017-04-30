from sqlalchemy import create_engine

from models import Base
from scripts import pg_url


def setup_database():
    engine = create_engine(pg_url, echo=True)
    Base.metadata.create_all(bind=engine)

    # install_user_table_functions(session)
    #
    # install_login_function(session)
    # for schema, table in [('api', 'messages')]:
    #     setup_table_notifications(session, schema, table)


if __name__ == '__main__':
    setup_database()
