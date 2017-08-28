from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,
                        UniqueConstraint, text)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from general.database.util import Base


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
    is_sortable = Column(Boolean, default=True)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer)

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)

    user = relationship('Users')
