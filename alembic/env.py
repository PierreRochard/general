import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

sys.path.append('.')
from postgrest_boilerplate.models import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    return URL(drivername='postgresql+psycopg2',
               username=os.environ['PGREST_DB_ADMIN_USER'],
               password=os.environ['PGREST_DB_ADMIN_PASSWORD'],
               host=os.environ['PGREST_DB_HOST'],
               port=os.environ['PGREST_DB_PORT'],
               database=os.environ['PGREST_DB_NAME'],
               query=None)


def run_migrations_offline():
    url = get_url()
    context.configure(url=url,
                      target_metadata=target_metadata,
                      literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(get_url())

    with engine.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
