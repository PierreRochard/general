from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'admin'}

    id = Column(UUID(as_uuid=True),
                server_default=text('uuid_generate_v4()'),
                primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    active = Column(Boolean)
    confirmed_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))
    current_login_at = Column(DateTime(timezone=True))
    last_login_ip = Column(String)
    current_login_ip = Column(String)
    login_count = Column(Integer)
