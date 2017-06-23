from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID

from .util import Base


class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = {'schema': 'api'}

    id = Column(UUID(as_uuid=True),
                server_default=text('gen_random_uuid()'),
                primary_key=True)
    time = Column(DateTime, nullable=False, server_default=text('now()'))
    from_user = Column(String, nullable=False,
                       server_default=text('current_user'))
    to_user = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String)


def create_api_items(session):
    session.execute("""
    CREATE OR REPLACE VIEW api.items AS 
      SELECT coalesce(ts.custom_name,
                      t.table_name) AS label,
             ts.icon AS icon,
             ts.id AS id,
             ts.submenu_id AS submenu_id,
             string_to_array('/' || ts.table_name, ' ') 
                AS "routerLink",
             ts.is_visible,
             ts.order_index
      FROM admin.tables t
      LEFT OUTER JOIN admin.table_settings ts
          ON t.table_name = ts.table_name
          AND ts.user = current_user
      WHERE current_user != 'anon'
      UNION
      SELECT coalesce(fs.custom_name,
      f.form_name) as label,
      fs.icon,
      fs.id,
      fs.submenu_id AS submenu_id,
             string_to_array('/rpc/' || fs.form_name, ' ') 
                AS "routerLink",
      fs.is_visible,
      fs.order_index
      FROM admin.forms f
      LEFT OUTER JOIN admin.form_settings fs
        ON f.form_name = fs.form_name
        AND fs.user = current_user
      WHERE (current_user != 'anon' AND f.form_name != 'login')
         OR (current_user  = 'anon' AND f.form_name  = 'login')
      ORDER BY order_index ASC NULLS LAST, label ASC NULLS LAST;
    GRANT SELECT ON api.items TO anon;
          """)


def create_api_submenus(session):
    session.execute("""
    CREATE OR REPLACE VIEW api.menubar AS
     SELECT s.id,
            s.submenu_name AS label,
            s.icon,
            string_to_array('', '') as "routerLink",
            s.is_visible,
            s.order_index
     FROM admin.submenus s
     WHERE s.user = current_user
       AND current_user != 'anon'
     UNION
     SELECT i.id,
            i.label,
            i.icon, 
            i."routerLink",
            i.is_visible,
            i.order_index
     FROM api.items i
     WHERE i.submenu_id IS NULL
     ORDER BY order_index ASC NULLS LAST, label ASC NULLS LAST;
     
     GRANT SELECT, UPDATE, INSERT ON api.menubar TO anon;
    """)


def create_api_datatable_view(session):
    session.execute("""
      CREATE OR REPLACE VIEW api.datatable AS
        SELECT c.table_name, 
               c.column_name as field, 
               coalesce(cs.custom_name, c.column_name) as header,
               cs.order_index
        FROM admin.columns c
          LEFT OUTER JOIN admin.table_column_settings cs
            ON c.table_name = cs.table_name
               AND c.column_name = cs.column_name
               AND cs.user = current_user
      ORDER BY order_index ASC NULLS LAST, field ASC NULLS LAST;
    """)


def create_api_table_settings(session):
    session.execute("""
    CREATE OR REPLACE VIEW api.table_settings AS 
      SELECT t.table_name, 
             ts.id,
             ts.user,
             ts.custom_name,
             ts.submenu_id,
             ts.icon,
             ts.is_visible,
             ts.can_insert,
             ts.can_update,
             ts.can_delete,
             ts.order_index
      FROM admin.tables t
      LEFT OUTER JOIN admin.table_settings ts
          ON t.table_name = ts.table_name
          AND ts.user = current_user
      ORDER BY ts.order_index ASC NULLS LAST, t.table_name ASC NULLS LAST;
    
    DROP TRIGGER IF EXISTS table_settings_trigger ON api.table_settings;
    CREATE TRIGGER table_settings_trigger
        INSTEAD OF INSERT OR UPDATE OR DELETE
        ON api.table_settings
        FOR EACH ROW
    EXECUTE PROCEDURE admin.table_settings_function();
     GRANT SELECT ON api.table_settings TO anon;
    """)


def create_api_column_settings(session):
    session.execute("""
    CREATE OR REPLACE VIEW api.table_column_settings AS 
      SELECT c.table_name,
             c.column_name,
             c.is_nullable,
             c.column_default,
             c.data_type,
             tcs.id,
             tcs.user,
            
             tcs.can_update,
             tcs.custom_name,
             tcs.format,
             tcs.order_index,
             tcs.is_visible
      FROM admin.columns c
      LEFT OUTER JOIN admin.table_column_settings tcs
          ON c.table_name = tcs.table_name
          AND c.column_name = tcs.column_name
          AND tcs.user = current_user;
        
      DROP TRIGGER IF EXISTS column_settings_trigger ON api.table_column_settings;
      CREATE TRIGGER column_settings_trigger
      INSTEAD OF INSERT OR UPDATE OR DELETE
      ON api.table_column_settings
      FOR EACH ROW
      EXECUTE PROCEDURE admin.table_column_settings_function();
    """)


def create_api_form_settings(session):
    session.execute("""
        CREATE OR REPLACE VIEW api.form_settings AS 
          SELECT f.form_name,
                 f.form_args,
                 f.form_arg_types,
                 fs.id,
                 fs.user,
                
                 fs.custom_name,
                 fs.submenu_id,
                 fs.icon,
                 fs.is_visible
          FROM admin.forms f
          LEFT OUTER JOIN admin.form_settings fs
              ON f.form_name = fs.form_name
              AND fs."user" = current_user;
      
      DROP TRIGGER IF EXISTS form_settings_trigger ON api.form_settings;
      CREATE TRIGGER form_settings_trigger
      INSTEAD OF INSERT OR UPDATE OR DELETE
      ON api.form_settings
      FOR EACH ROW
      EXECUTE PROCEDURE admin.form_settings_function();
    """)


def create_api_form_field_settings(session):
    session.execute("""
        CREATE OR REPLACE VIEW api.form_field_settings AS 
          SELECT f.form_name,
                 unnest(f.form_args) as form_field_name
          FROM admin.forms f;
     GRANT SELECT ON api.form_field_settings TO anon;
    """)
