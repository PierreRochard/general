from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, 
                        UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from general.database.util import Base


class Submenus(Base):
    __tablename__ = 'submenus'
    __table_args__ = (UniqueConstraint('user_id',
                                       'submenu_name',
                                       name='submenus_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    submenu_name = Column(String, nullable=False)
    icon = Column(String)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer, default=2)

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)

    user = relationship('Users')
