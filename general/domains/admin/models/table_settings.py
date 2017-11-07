from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, text,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID

from general.database.base import Base


class TableSettings(Base):
    __tablename__ = 'table_settings'
    __table_args__ = (UniqueConstraint('user_id',
                                       'schema_name',
                                       'table_name',
                                       name='table_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    schema_name = Column(String, nullable=False)
    table_name = Column(String, nullable=False)

    can_archive = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    can_insert = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    custom_name = Column(String)
    submenu_id = Column(UUID, ForeignKey('admin.submenus.id'))
    icon = Column(String)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer)
    row_limit = Column(Integer, default=10)
    row_offset = Column(Integer, default=0)
    sort_column = Column(String)
    sort_order = Column(Integer)

    # Feature Utility Columns
    mapping_column_name = Column(String)
    mapping_table_name = Column(String)
    mapping_schema_name = Column(String)
    keyword_column_name = Column(String)

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)
