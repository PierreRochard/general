from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    String,
    text,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID

from general.database.base import Base


class DialogSettings(Base):
    __tablename__ = 'dialog_settings'
    __table_args__ = (UniqueConstraint('user_id',
                                       'name',
                                       name='dialog_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)

    name = Column(String, nullable=False)

    header = Column(String, default='Dialog')

    is_draggable = Column(Boolean, default=False)
    is_resizable = Column(Boolean, default=False)
    # Defines if background should be blocked when dialog is displayed.
    is_modal = Column(Boolean, default=True)
    # Specifies if clicking the modal background should hide the dialog.
    is_dismissible = Column(Boolean, default=True)

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)
