import os
import sys
from logging.config import fileConfig
from pprint import pformat

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.schema import SchemaItem, Table

sys.path.append('.')

from general.database.util import Base
import general.domains.admin.models
import general.domains.auth.models

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def before_cursor_execute(conn, cursor, statement, parameters, context,
                          executemany):
    # schema_names = ['admin', 'auth', ]
    # schema_names = ','.join(schema_names)
    # statement = f'SET search_path TO {schema_names}; {statement}'
    # print(statement)
    return statement, parameters


def include_object(object_, name, type_, reflected, compare_to):
    schemas = ['admin', 'auth']
    if str(object_).split('.')[0] in schemas:
        return True
    else:
        if isinstance(object_, Table):
            return False
        if object_.table.schema in schemas:
            return True
        else:
            print('-----')
            print(type(object_))
            print(object_)
            print(object_.table.schema)
            print(pformat(dir(object_)))
            print(pformat(dir(object_.table)))
            print(name)
            print(type_)
            print(reflected)
            print(compare_to)
            print('-----')
            raise Exception()


def get_url():
    return URL(drivername='postgresql+psycopg2',
               username=os.environ['PGUSER'],
               password=os.environ['PGPASSWORD'],
               host=os.environ['PGHOST'],
               port=os.environ['PGPORT'],
               database=os.environ['PGDATABASE'],
               query=None)


def run_migrations_offline():
    url = get_url()
    context.configure(url=url,
                      target_metadata=target_metadata,
                      literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


listen(Engine, 'before_cursor_execute', before_cursor_execute, retval=True)


def run_migrations_online():
    engine = create_engine(get_url())

    with engine.connect() as connection:
        context.configure(connection=connection,
                          include_schemas=True,
                          include_object=include_object,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
