from general.database.util import session_scope


def create_forms_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.forms CASCADE;
        """)
        session.execute("""
          CREATE OR REPLACE VIEW admin_api.forms AS
            SELECT (row_number() OVER())::INT id, *
            FROM (
                SELECT dfs.form_name AS name, 
                       dfs.custom_name AS custom_name
                FROM admin.default_form_settings dfs
                WHERE dfs.user = current_user
            ) sub;
        """)

