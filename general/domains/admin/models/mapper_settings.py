from sqlalchemy import Column, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID

from general.database.base import Base


class MapperSettings(Base):
    __tablename__ = 'mapper_settings'
    __table_args__ = (UniqueConstraint('user_id',
                                       'table_settings_id',
                                       name='mapper_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    table_settings_id = Column(UUID,
                               ForeignKey('admin.table_settings.id'),
                               nullable=False)

    title = Column(String)

    # The keyword that the user is currently filtering for
    keyword = Column(String)

    # The column that we are filtering with a keyword, it belongs to the same table
    # as the table_settings_id above
    filter_column_settings_id = Column(UUID, ForeignKey(
        'admin.table_column_settings.id'))

    # The column that has all the items we can map to
    mapping_column_settings_id = Column(UUID, ForeignKey(
        'admin.table_column_settings.id'))

    # The column that will store the saved mapping's keyword
    saved_keyword_column_settings_id = Column(UUID, ForeignKey(
        'admin.table_column_settings.id'))

    # The column that will store the saved mapping's value
    saved_mapping_column_settings_id = Column(UUID, ForeignKey(
        'admin.table_column_settings.id'))

    user_id = Column(UUID,
                     ForeignKey('auth.users.id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                     nullable=False)
