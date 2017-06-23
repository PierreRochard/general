from sqlalchemy import (Column, String, text, UniqueConstraint,
                        Integer, Boolean, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID

from models.util import Base, session_scope


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
    order_index = Column(Integer)


def create_admin_tables_view():
    with session_scope() as session:
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
