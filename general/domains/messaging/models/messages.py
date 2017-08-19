from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID

from general.database.util import Base


class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = {'schema': 'messaging'}

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    time = Column(DateTime, nullable=False, server_default=text('now()'))
    from_user = Column(String, nullable=False,
                       server_default=text('current_user'))
    to_user = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String)
