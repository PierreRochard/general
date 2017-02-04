from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def get_session():
    from mech_ops.webapp.config import DevConfig
    engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI, echo=True)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    return session
