from contextlib import contextmanager
import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.orm import sessionmaker


@contextmanager
def session_scope(echo=False,
                  raise_integrity_error=True,
                  raise_programming_error=True,
                  engine=None):
    """Provide a transactional scope around a series of operations."""
    if engine is None:
        pg_url = URL.create(
            drivername='postgresql+psycopg2',
            username=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'],
            host=os.environ['PGHOST'],
            port=int(os.environ['PGPORT']),
            query={},
            database=os.environ['PGDB']
        )
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
