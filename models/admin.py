from sqlalchemy import Column, String, text, UniqueConstraint, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID

from .util import Base


class TableSettings(Base):
    __tablename__ = 'table_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'table_name',
                                       name='table_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String)
    table_name = Column(String)
    custom_name = Column(String)
    category = Column(String)
    visible = Column(Boolean)


def setup_table_settings_views(session):
    session.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS tables AS
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'api';
        
        REFRESH MATERIALIZED VIEW tables;
    """)


class ColumnSettings(Base):
    __tablename__ = 'column_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'table_name',
                                       'column_name',
                                       name='column_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String)
    table_name = Column(String)
    column_name = Column(String)
    custom_name = Column(String)
    index = Column(Integer)
    format = Column(String)
    visible = Column(Boolean)


def setup_column_settings_views(session):
    session.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS columns AS
        SELECT table_name, column_name, is_nullable, data_type
        FROM information_schema.columns
        WHERE table_schema = 'api'

        REFRESH MATERIALIZED VIEW columns;
    """)
