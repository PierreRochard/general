from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    text,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID

from general.database.base import Base


class ContextMenuItems(Base):
    __tablename__ = 'context_menu_items'
    __table_args__ = (UniqueConstraint('user_id',
                                       'schema_name',
                                       'table_name',
                                       'label',
                                       name='context_menu_items_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    schema_name = Column(String, nullable=False)
    table_name = Column(String, nullable=False)

    label = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    command = Column(String)

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)
