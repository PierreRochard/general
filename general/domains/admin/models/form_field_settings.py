from sqlalchemy import (Column, ForeignKey, Integer, String, text,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from general.database.util import Base


class FormFieldSettings(Base):
    __tablename__ = 'form_field_settings'
    __table_args__ = (UniqueConstraint('user_id',
                                       'form_name',
                                       'form_field_name',
                                       name='form_field_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)

    form_name = Column(String)
    form_field_name = Column(String)
    custom_name = Column(String)
    order_index = Column(Integer)

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)

    user = relationship('Users')
