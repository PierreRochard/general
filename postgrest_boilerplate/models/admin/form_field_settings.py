from sqlalchemy import Column, Integer, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID

from postgrest_boilerplate.models.util import Base


class FormFieldSettings(Base):
    __tablename__ = 'form_field_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'form_name',
                                       'form_field_name',
                                       name='form_field_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    form_name = Column(String)
    form_field_name = Column(String)
    custom_name = Column(String)
    order_index = Column(Integer)
