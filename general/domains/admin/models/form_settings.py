from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,
                        UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from general.database.base import Base


class FormSettings(Base):
    __tablename__ = 'form_settings'
    __table_args__ = (UniqueConstraint('user_id',
                                       'schema_name',
                                       'form_name',
                                       name='form_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    schema_name = Column(String, nullable=False)
    form_name = Column(String, nullable=False)
    custom_name = Column(String)
    submenu_id = Column(UUID, ForeignKey('admin.submenus.id'))
    icon = Column(String)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer)

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)

    user = relationship('Users')
