from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

from .util import Base


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    active = Column(Boolean)
    confirmed_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))
    current_login_at = Column(DateTime(timezone=True))
    last_login_ip = Column(String)
    current_login_ip = Column(String)
    login_count = Column(Integer)


class NotificationChannels(Base):
    __tablename__ = 'notification_channels'
    __table_args__ = {'schema': 'auth'}

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    channel_name = Column(String, unique=True)
    table = Column(String)
    schema = Column(String)
    jwt = Column(String)
