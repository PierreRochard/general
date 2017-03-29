from sqlalchemy import Column, String, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from .util import Base


class Settings(Base):
    __tablename__ = 'users'
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
