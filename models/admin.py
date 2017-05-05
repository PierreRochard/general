from sqlalchemy import Column, String, text, UniqueConstraint, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID

from .util import Base


class TableSettings(Base):
    __tablename__ = 'table_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'table_name',
                                       name='table_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String)
    table_name = Column(String)
    custom_name = Column(String)
    category = Column(String)
    visible = Column(Boolean)


def setup_table_settings_views(session):
    session.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS admin.tables AS
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'api';
        
        REFRESH MATERIALIZED VIEW admin.tables;
    """)
    # https://www.postgresql.org/docs/current/static/rules-views.html
    session.execute("""
        CREATE OR REPLACE VIEW api.table_settings AS 
          SELECT admin.tables.table_name, admin.table_settings.* FROM admin.tables
          LEFT OUTER JOIN admin.table_settings 
              ON admin.tables.table_name = admin.table_settings.table_name
    """)


# CREATE FUNCTION MyFuncName() RETURNS trigger AS $$
# DECLARE
#   id integer;
# BEGIN
#   INSERT INTO tableA (time) VALUES COALESCE(NEW.time, NOW()) RETURNING aPrimaryKey INTO id;
#   INSERT INTO tableB (aPrimaryKey, someCol1) VALUES (id, NEW.someValue);
#   RETURN NEW;
# END; $$ LANGUAGE PLPGSQL;
#
# CREATE TRIGGER MyView_on_insert INSTEAD OF INSERT ON MyView
#   FOR EACH ROW EXECUTE PROCEDURE MyFuncName();

class ColumnSettings(Base):
    __tablename__ = 'column_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'table_name',
                                       'column_name',
                                       name='column_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String)
    table_name = Column(String)
    column_name = Column(String)
    custom_name = Column(String)
    index = Column(Integer)
    format = Column(String)
    visible = Column(Boolean)


def setup_column_settings_views(session):
    session.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS admin.columns AS
            SELECT table_name, column_name, is_nullable, data_type
            FROM information_schema.columns
            WHERE table_schema = 'api'

        REFRESH MATERIALIZED VIEW admin.columns;
    """)
    # https://www.postgresql.org/docs/current/static/rules-views.html
    session.execute("""
        CREATE OR REPLACE VIEW api.column_settings AS 
          SELECT admin.columns.table_name,
                 admin.columns.column_name,
                 admin.columns.is_nullable,
                 admin.columns.data_type,
                 admin.column_settings.* FROM admin.columns
          LEFT OUTER JOIN admin.column_settings 
              ON admin.columns.table_name = admin.column_settings.table_name
              AND admin.columns.column_name = admin.column_settings.column_name
    """)
