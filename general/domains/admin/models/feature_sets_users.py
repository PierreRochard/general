from sqlalchemy import (Column, ForeignKey, text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID

from general.database.util import Base
from general.domains.auth.models.users import Users


class FeatureSetsUsers(Base):
    __tablename__ = 'feature_sets_users'
    __table_args__ = (UniqueConstraint('feature_set_id',
                                       'user_id',
                                       name='feature_sets_users_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)

    feature_set_id = Column(UUID,
                            ForeignKey('admin.feature_sets.id',
                                       onupdate='CASCADE',
                                       ondelete='CASCADE'),
                            nullable=False)

    user_id = Column(UUID,
                     ForeignKey(Users.id,
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)
