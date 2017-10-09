from sqlalchemy import (Boolean, Column, ForeignKey, Numeric, Integer, String,
                        UniqueConstraint, text)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from general.database.base import Base


class TableColumnSettings(Base):
    __tablename__ = 'table_column_settings'
    __table_args__ = (UniqueConstraint('user_id',
                                       'schema_name',
                                       'table_name',
                                       'column_name',
                                       name='table_column_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    schema_name = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    column_name = Column(String, nullable=False)

    can_update = Column(Boolean)
    custom_name = Column(String)
    filter_match_mode = Column(String, default='contains')
    filter_value = Column(String)
    format_pattern = Column(String)
    input_type = Column(String, default='text')
    is_filterable = Column(Boolean, default=False)
    is_multiple = Column(Boolean, default=False)
    is_select_item = Column(Boolean, default=False)
    is_sortable = Column(Boolean, default=True)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer)
    select_item_label_column_name = Column(String)
    select_item_schema_name = Column(String)
    select_item_table_name = Column(String)
    select_item_value_column_name = Column(String)
    suggestion_column_name = Column(String)
    suggestion_schema_name = Column(String)
    suggestion_table_name = Column(String)

    # CSS Properties, in pixels
    height = Column(Numeric)
    overflow = Column(String)
    padding_bottom = Column(Numeric)
    padding_left = Column(Numeric)
    padding_right = Column(Numeric)
    padding_top = Column(Numeric)
    width = Column(Numeric)

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)

    user = relationship('Users')
