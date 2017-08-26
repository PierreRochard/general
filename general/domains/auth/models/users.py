from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

from general.database.util import Base, session_scope


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}

    id = Column(UUID,
                server_default=text('auth.gen_random_uuid()'),
                primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    active = Column(Boolean, nullable=False)
    confirmed_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))
    current_login_at = Column(DateTime(timezone=True))
    last_login_ip = Column(String)
    current_login_ip = Column(String)
    login_count = Column(Integer)

    @staticmethod
    def create_constraint_triggers_on_users():
        with session_scope() as session:
            session.execute("""
            DROP TRIGGER IF EXISTS ensure_user_role_exists
            ON auth.users;
            CREATE CONSTRAINT TRIGGER ensure_user_role_exists
            AFTER INSERT OR UPDATE ON auth.users
            FOR EACH ROW
            EXECUTE PROCEDURE auth.check_if_role_exists();
            """)

    @staticmethod
    def create_triggers_on_users():
        with session_scope() as session:
            session.execute("""
            DROP TRIGGER IF EXISTS encrypt_password
            ON auth.users;
            CREATE TRIGGER encrypt_password
            BEFORE INSERT OR UPDATE ON auth.users
            FOR EACH ROW
            EXECUTE PROCEDURE auth.encrypt_password();
            """)
