from postgrest_boilerplate.database.util import session_scope


def grant_privileges_on_users():
    with session_scope() as session:
        session.execute("GRANT SELECT ON TABLE auth.users TO anon;")
