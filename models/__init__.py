from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def get_session(database, user):
    engine = create_engine(f'postgresql+psycopg2://{user}@localhost:5432/{database}', echo=True)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    return session
