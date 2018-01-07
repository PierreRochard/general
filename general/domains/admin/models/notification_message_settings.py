from sqlalchemy import (Boolean, Column, String, text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID

from general.database.base import Base


class NotificationMessageSettings(Base):
    __tablename__ = 'notification_message_settings'
    __table_args__ = (UniqueConstraint('namespace',
                                       'message_type',
                                       name='notification_message_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    namespace = Column(String, nullable=False)
    message_type = Column(String, nullable=False)

    is_visible = Column(Boolean, nullable=False, default=False)
    severity = Column(String, nullable=False, default='info')
    summary = Column(String)
    detail = Column(String)
