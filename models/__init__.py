from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def get_session():
    engine = create_engine("postgresql+psycopg2://postgrest@localhost:5432/rest", echo=True)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    return session
