from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, \
    UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID

from postgrest_boilerplate.database.util import Base, session_scope


class FormSettings(Base):
    __tablename__ = 'form_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'form_name',
                                       name='form_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    form_name = Column(String)
    custom_name = Column(String)
    submenu_id = Column(UUID, ForeignKey('admin.submenus.id'))
    icon = Column(String)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer)


def create_admin_forms_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.forms CASCADE;
            CREATE MATERIALIZED VIEW admin.forms AS
                SELECT pg_proc.proname as form_name,
                       pg_proc.proargnames as form_args,
                       pg_proc.proargtypes AS form_arg_types
                FROM pg_proc
                LEFT OUTER JOIN pg_namespace ON pg_namespace.OID = pg_proc.pronamespace
                WHERE pg_namespace.nspname = 'api';
        """)

