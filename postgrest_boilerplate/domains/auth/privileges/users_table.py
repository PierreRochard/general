from postgrest_boilerplate.database.util import session_scope


def grant_privileges_on_users():
    with session_scope(raise_programming_error=True) as session:
        session.execute("GRANT USAGE ON SCHEMA api TO anon;")
        session.execute("GRANT SELECT ON TABLE auth.users TO anon;")
