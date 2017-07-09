# Todo: there are namespacing problems with extensions
# Fix this in ansible, not in here
# Dirty hack is to add schemas to the search path in postgres config
# session.execute("""
# CREATE EXTENSION pgcrypto SCHEMA auth;
# CREATE EXTENSION pgjwt SCHEMA auth;
# """)