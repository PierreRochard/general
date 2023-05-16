from contextlib import contextmanager
import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.orm import sessionmaker


@contextmanager
def session_scope(echo=False,
                  raise_integrity_error=True,
                  raise_programming_error=True):
    """Provide a transactional scope around a series of operations."""
    pg_url = URL(drivername='postgresql+psycopg2',
                 username=os.environ['PGUSER'],
                 password=os.environ['PGPASSWORD'],
                 host=os.environ['PGHOST'],
                 port=os.environ['PGPORT'],
                 database=os.environ['PGDB'])
    engine = create_engine(pg_url, echo=echo)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    try:
        yield session
        session.commit()
    except IntegrityError:
        session.rollback()
        if raise_integrity_error:
            raise
    except ProgrammingError:
        session.rollback()
        if raise_programming_error:
            raise
    except:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def mssql_session_scope(echo=False,
                        raise_integrity_error=True,
                        raise_programming_error=True):
    """Provide a transactional scope around a series of operations."""
    ms_url = URL(drivername='mssql+pyodbc',
                 username=os.environ['MSSQL_USER'],
                 password=os.environ['PGPASSWORD'],
                 host=os.environ['MSSQL_HOST'],
                 port=os.environ['MSSQL_PORT'],
                 database=os.environ['MSSQL_DB'],
                 query={'driver': 'ODBC Driver 18 for SQL Server',
                        'TrustServerCertificate': 'yes'})
    engine = create_engine(ms_url, echo=echo)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    try:
        yield session
        session.commit()
    except IntegrityError:
        session.rollback()
        if raise_integrity_error:
            raise
    except ProgrammingError:
        session.rollback()
        if raise_programming_error:
            raise
    except:
        session.rollback()
        raise
    finally:
        session.close()
