from sqlalchemy import (Column, String, text, UniqueConstraint,
                        Integer, Boolean, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID

from .util import Base


class Submenus(Base):
    __tablename__ = 'submenus'
    __table_args__ = (UniqueConstraint('user',
                                       'submenu_name',
                                       name='submenus_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    submenu_name = Column(String, nullable=False)
    icon = Column(String)
    is_visible = Column(Boolean, default=True)


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
    table_name = Column(String, nullable=False)

    can_delete = Column(Boolean, default=True)
    can_insert = Column(Boolean, default=True)
    can_update = Column(Boolean, default=True)
    custom_name = Column(String)
    submenu_id = Column(UUID, ForeignKey('admin.submenus.id'))
    icon = Column(String)
    is_visible = Column(Boolean, default=True)


def create_admin_tables_view(session):
    session.execute("""
        DROP MATERIALIZED VIEW IF EXISTS admin.tables CASCADE;
        CREATE MATERIALIZED VIEW admin.tables AS
            SELECT pg_class.relname AS "table_name", 
                   pg_class.relkind AS "kind"
            FROM pg_class
              JOIN pg_namespace ON 	pg_namespace.oid = pg_class.relnamespace
            WHERE pg_namespace.nspname = 'api' 
            AND pg_class.relkind IN ('v', 'm', 'r');
    """)

    session.execute("""
    CREATE OR REPLACE FUNCTION admin.table_settings_function()
      RETURNS TRIGGER AS
            $BODY$
               BEGIN
                IF TG_OP = 'INSERT' THEN
                    INSERT INTO admin.table_settings 
                                        (table_name,
                                          can_delete,
                                          can_insert,
                                          can_update,
                                          custom_name,
                                          submenu_id,
                                          icon,
                                          is_visible) 
                                  VALUES(NEW.table_name,
                                         NEW.can_delete,
                                         NEW.can_insert,
                                         NEW.can_update,
                                         NEW.custom_name,
                                         NEW.submenu_id,
                                         NEW.icon,
                                         NEW.is_visible);
                    RETURN NEW;
                  ELSIF TG_OP = 'UPDATE' THEN
                      UPDATE admin.table_settings SET 
                             can_delete=NEW.can_delete, 
                             can_insert=NEW.can_insert, 
                             can_update=NEW.can_update, 
                             custom_name=NEW.custom_name, 
                             submenu_id=NEW.submenu_id, 
                             icon=NEW.icon, 
                             is_visible=NEW.is_visible 
                      WHERE id=OLD.id;
                    -- INSERT INTO admin.table_settings (custom_name) VALUES(NEW.custom_name);
                   RETURN NEW;
                  ELSIF TG_OP = 'DELETE' THEN
                   DELETE 
                     FROM admin.table_settings 
                   WHERE id=OLD.id;
                   RETURN NULL; 
                END IF;
                RETURN NEW;
              END;
            $BODY$
      LANGUAGE plpgsql VOLATILE
      COST 100;
    """)
    # Create default settings records
    # session.execute("""
    #     CREATE OR REPLACE FUNCTION admin.create_defaults_function()
    #     RETURNS VOID AS $$
    #       DECLARE
    #       pg_users RECORD[];
    #       tables RECORD[];
    #       BEGIN
    #         SELECT information_schema
    #         <<users_loop>>
    #         FOREACH pg_user IN ARRAY pg_users
    #           LOOP
    #             <<periods_loop>>
    #              FOR period_name in SELECT DISTINCT
    #                       to_char(bookkeeping.journal_entries.timestamp,
    #                       period_interval_name) AS p
    #                 FROM bookkeeping.journal_entries
    #                 WHERE bookkeeping.journal_entries.timestamp >= new.timestamp LOOP
    #               PERFORM bookkeeping.update_trial_balance(
    #                     new.debit_subaccount,
    #                     period_interval_name,
    #                     period_name.p);
    #               PERFORM bookkeeping.update_trial_balance(
    #                     new.credit_subaccount,
    #                     period_interval_name,
    #                     period_name.p);
    #             END LOOP periods_loop;
    #           END LOOP period_interval_loop;
    #         RETURN new;
    #       END;
    #     $$
    #     SECURITY DEFINER
    #     LANGUAGE  plpgsql;
    #     """)


class TableColumnSettings(Base):
    __tablename__ = 'table_column_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'table_name',
                                       'column_name',
                                       name='table_column_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    table_name = Column(String, nullable=False)
    column_name = Column(String, nullable=False)

    can_update = Column(Boolean)
    custom_name = Column(String)
    format = Column(String)
    index = Column(Integer)
    is_visible = Column(Boolean)


def create_admin_columns_view(session):
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

    session.execute("""
    CREATE OR REPLACE FUNCTION admin.table_column_settings_function()
      RETURNS TRIGGER AS
            $BODY$
               BEGIN
                IF TG_OP = 'INSERT' THEN
                    INSERT INTO admin.table_column_settings 
                                          (table_name,
                                           column_name,
                                           
                                           can_update,
                                           custom_name,
                                           format,
                                           index,
                                           is_visible) 
                                  VALUES(NEW.table_name,
                                         NEW.column_name,
                                         
                                         NEW.can_update,
                                         NEW.custom_name,
                                         NEW.format,
                                         NEW.index,
                                         NEW.is_visible);
                    RETURN NEW;
                  ELSIF TG_OP = 'UPDATE' THEN
                    UPDATE admin.table_column_settings SET 
                           can_update=NEW.can_update,
                           custom_name=NEW.custom_name,
                           format=NEW.format,
                           index=NEW.index,
                           is_visible=NEW.is_visible  
                        WHERE id=OLD.id;
                   RETURN NEW;
                  ELSIF TG_OP = 'DELETE' THEN
                   DELETE 
                      FROM admin.table_column_settings 
                   WHERE id=OLD.id;
                   RETURN NULL; 
                END IF;
                RETURN NEW;
              END;
            $BODY$
      LANGUAGE plpgsql VOLATILE
      COST 100;
    """)


class FormSettings(Base):
    __tablename__ = 'form_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'form_name',
                                       name='form_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    form_name = Column(String)
    custom_name = Column(String)
    submenu_id = Column(UUID, ForeignKey('admin.submenus.id'))
    icon = Column(String)
    is_visible = Column(Boolean, default=True)


class FormFieldSettings(Base):
    __tablename__ = 'form_field_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'form_name',
                                       'form_field_name',
                                       name='form_field_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    form_name = Column(String)
    form_field_name = Column(String)
    custom_name = Column(String)


def create_admin_forms_view(session):
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

    session.execute("""
    CREATE OR REPLACE FUNCTION admin.form_settings_function()
      RETURNS TRIGGER AS
            $BODY$
               BEGIN
                IF TG_OP = 'INSERT' THEN
                    INSERT INTO admin.form_settings (form_name,

                                                       custom_name,
                                                       submenu_id,
                                                       icon,
                                                       is_visible)
                                              VALUES(NEW.form_name,

                                                     NEW.custom_name,
                                                     NEW.submenu_id,
                                                     NEW.icon,
                                                     NEW.is_visible);
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
    """)
