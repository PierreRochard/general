from __future__ import with_statement
from logging.config import fileConfig
import os

from alembic import context
import keyring
from sqlalchemy import create_engine


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.


config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from models import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    try:
        username = keyring.get_password('PGUSER', 'PGUSER')
        password = keyring.get_password('PGPASSWORD', 'PGPASSWORD')
        host = keyring.get_password('PGHOST', 'PGHOST')
        port = keyring.get_password('PGPORT', 'PGPORT')
        database = keyring.get_password('PGDATABASE', 'PGDATABASE')
    except RuntimeError:
        username = os.environ['PGUSER']
        password = os.environ['PGPASSWORD']
        host = os.environ['PGHOST']
        port = os.environ['PGPORT']
        database = os.environ['PGDATABASE']

    URL = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'

    return URL


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(url=url,
                      target_metadata=target_metadata,
                      literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectible = create_engine(get_url())

    with connectible.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
