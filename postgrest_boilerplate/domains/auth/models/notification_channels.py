from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID

from postgrest_boilerplate.database.util import Base


class NotificationChannels(Base):
    __tablename__ = 'notification_channels'
    __table_args__ = {'schema': 'auth'}

    id = Column(UUID(as_uuid=True),
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    channel_name = Column(String, unique=True)
    table = Column(String)
    schema = Column(String)
    jwt = Column(String)
