import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

pg_url = URL(drivername='postgresql+psycopg2',
             username=os.environ['PGUSER'],
             password=os.environ['PGPASSWORD'],
             host=os.environ['PGHOST'],
             port=os.environ['PGPORT'],
             database='rest')


def get_session():
    engine = create_engine(pg_url, echo=True)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    return session
