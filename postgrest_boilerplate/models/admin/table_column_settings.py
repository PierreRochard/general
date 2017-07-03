from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID

from postgrest_boilerplate.models.util import Base, session_scope


class TableColumnSettings(Base):
    __tablename__ = 'table_column_settings'
    __table_args__ = (UniqueConstraint('user',
                                       'table_name',
                                       'column_name',
                                       name='table_column_settings_unique_constraint'),
                      {'schema': 'admin'},
                      )

    id = Column(UUID(as_uuid=True),
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    user = Column(String,
                  nullable=False,
                  server_default=text('current_user'))
    table_name = Column(String, nullable=False)
    column_name = Column(String, nullable=False)

    can_update = Column(Boolean)
    custom_name = Column(String)
    filter_match_mode = Column(String, default='contains')
    filter_value = Column(String)
    format_pattern = Column(String)
    is_filterable = Column(Boolean, default=True)
    is_sortable = Column(Boolean, default=True)
    is_visible = Column(Boolean, default=True)
    order_index = Column(Integer)


def create_admin_columns_view():
    with session_scope() as session:
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
