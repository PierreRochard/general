import os

from sqlalchemy.engine.url import URL

pg_url = URL(drivername='postgresql+psycopg2',
             username=os.environ['PGUSER'],
             password=os.environ['PGPASSWORD'],
             host=os.environ['PGHOST'],
             port=os.environ['PGPORT'],
             database='rest')