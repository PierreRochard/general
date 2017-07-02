from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, \
    UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID

from postgrest_boilerplate.models.util import Base, session_scope


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
