from sqlalchemy import (Column, String, text, UniqueConstraint,
                        Integer, Boolean)
from sqlalchemy.dialects.postgresql import UUID

from models.util import Base


class Submenus(Base):
    __tablename__ = 'submenus'
    __table_args__ = (UniqueConstraint('user',
                                       'submenu_name',
                                       name='submenus_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    submenu_name = Column(String, nullable=False)
    icon = Column(String)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer)
