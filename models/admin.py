from sqlalchemy import Column, String, text, UniqueConstraint, Integer
from sqlalchemy.dialects.postgresql import UUID

from .util import Base


class Settings(Base):
    __tablename__ = 'settings'
    __table_args__ = (UniqueConstraint('user',
                                       'path',
                                       'property',
                                       'key',
                                       name='setting_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String)
    path = Column(String)
    property = Column(String)
    key = Column(String)
    value = Column(String)


class TableSettings(Base):
    __tablename__ = 'table_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'path',
                                       'property',
                                       'key',
                                       name='setting_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String)
    table_name = Column(String)
    column_name = Column(String)
    index = Column(Integer)
    format = Column(String)
