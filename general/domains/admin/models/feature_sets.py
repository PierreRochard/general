from sqlalchemy import (Column, String, text)
from sqlalchemy.dialects.postgresql import UUID

from general.database.base import Base


class FeatureSets(Base):
    __tablename__ = 'feature_sets'
    __table_args__ = ({'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)

    name = Column(String, unique=True)
