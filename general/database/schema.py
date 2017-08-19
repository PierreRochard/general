from general.database.util import session_scope


class Schema(object):

    @staticmethod
    def create_extension(schema_name, extension_name):
        with session_scope(raise_programming_error=True) as session:
            session.execute(f"""
                 CREATE EXTENSION {schema_name} SCHEMA {extension_name};
                """)

    @staticmethod
    def drop_extension(schema_name):
        with session_scope(raise_programming_error=True) as session:
            session.execute(f"""
                    DROP EXTENSION IF EXISTS {schema_name} CASCADE;
                """)
