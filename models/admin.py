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
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    table_name = Column(String)
    custom_name = Column(String)
    category = Column(String)
    visible = Column(Boolean)
    can_insert = Column(Boolean)
    can_update = Column(Boolean)
    can_delete = Column(Boolean)


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
          SELECT admin.tables.table_name, 
                 admin.table_settings.id,
                 admin.table_settings.user,
                 admin.table_settings.custom_name,
                 admin.table_settings.category,
                 admin.table_settings.visible,
                 admin.table_settings.can_insert,
                 admin.table_settings.can_update,
                 admin.table_settings.can_delete
          FROM admin.tables
          LEFT OUTER JOIN admin.table_settings 
              ON admin.tables.table_name = admin.table_settings.table_name
    """)

    session.execute("""
    CREATE OR REPLACE FUNCTION table_settings_function()
      RETURNS TRIGGER AS
            $BODY$
               BEGIN
                IF TG_OP = 'INSERT' THEN
                    INSERT INTO admin.table_settings (custom_name) VALUES(NEW.custom_name);
                    RETURN NEW;
                  ELSIF TG_OP = 'UPDATE' THEN
                   --UPDATE person_detail SET pid=NEW.pid, pname=NEW.pname WHERE pid=OLD.pid;
                   --UPDATE person_job SET pid=NEW.pid, job=NEW.job WHERE pid=OLD.pid;
                   RETURN NEW;
                  ELSIF TG_OP = 'DELETE' THEN
                   --DELETE FROM person_job WHERE pid=OLD.pid;
                   --DELETE FROM person_detail WHERE pid=OLD.pid;
                   RETURN NULL; 
                END IF;
                RETURN NEW;
              END;
            $BODY$
      LANGUAGE plpgsql VOLATILE
      COST 100;
      
    CREATE TRIGGER table_settings_trigger
      INSTEAD OF INSERT OR UPDATE OR DELETE
      ON api.table_settings
      FOR EACH ROW
      EXECUTE PROCEDURE table_settings_function();
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
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    table_name = Column(String)
    column_name = Column(String)
    custom_name = Column(String)
    index = Column(Integer)
    format = Column(String)
    visible = Column(Boolean)
    can_update = Column(Boolean)


def setup_column_settings_views(session):
    session.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS admin.columns AS
            SELECT table_name, column_name, is_nullable, data_type
            FROM information_schema.columns
            WHERE table_schema = 'api';

        REFRESH MATERIALIZED VIEW admin.columns;
    """)
    # https://www.postgresql.org/docs/current/static/rules-views.html
    session.execute("""
        CREATE OR REPLACE VIEW api.column_settings AS 
          SELECT admin.columns.table_name,
                 admin.columns.column_name,
                 admin.columns.is_nullable,
                 admin.columns.data_type,
                 admin.column_settings.id,
                 admin.column_settings.user,
                 admin.column_settings.custom_name,
                 admin.column_settings.index,
                 admin.column_settings.format,
                 admin.column_settings.visible,
                 admin.column_settings.can_update
          FROM admin.columns
          LEFT OUTER JOIN admin.column_settings 
              ON admin.columns.table_name = admin.column_settings.table_name
              AND admin.columns.column_name = admin.column_settings.column_name
    """)

    session.execute("""
    CREATE OR REPLACE FUNCTION column_settings_function()
      RETURNS TRIGGER AS
            $BODY$
               BEGIN
                  RETURN NEW;
                END;
            $BODY$
      LANGUAGE plpgsql VOLATILE
      COST 100;

    CREATE TRIGGER column_settings_trigger
      INSTEAD OF INSERT OR UPDATE OR DELETE
      ON api.column_settings
      FOR EACH ROW
      EXECUTE PROCEDURE column_settings_function();
    """)
