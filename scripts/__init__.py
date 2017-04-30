import os

from sqlalchemy.engine.url import URL


def get_pg_url():
    return URL(drivername='postgresql+psycopg2',
               username=os.environ['PGUSER'],
               password=os.environ['PGPASSWORD'],
               host=os.environ['PGHOST'],
               port=os.environ['PGPORT'],
               database='rest')
