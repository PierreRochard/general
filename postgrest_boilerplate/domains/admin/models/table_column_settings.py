from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID

from postgrest_boilerplate.database.util import Base, session_scope


class TableColumnSettings(Base):
    __tablename__ = 'table_column_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'table_name',
                                       'column_name',
                                       name='table_column_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    table_name = Column(String, nullable=False)
    column_name = Column(String, nullable=False)

    can_update = Column(Boolean)
    custom_name = Column(String)
    filter_match_mode = Column(String, default='contains')
    filter_value = Column(String)
    format_pattern = Column(String)
    is_filterable = Column(Boolean, default=True)
    is_sortable = Column(Boolean, default=True)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer)


def create_admin_columns_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.columns CASCADE;
            CREATE MATERIALIZED VIEW admin.columns AS
                SELECT table_name, 
                       column_name, 
                       is_nullable,
                       column_default,
                       data_type
                FROM information_schema.columns
                WHERE table_schema = 'api';
    
        """)
