from general.database.session_scope import session_scope


def create_home_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin_api.home CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin_api.home AS
         SELECT dhs.custom_name,
                dhs.headline,
                dhs.icon,
                dhs.sub_headline,
                dhs.supporting_image
         FROM admin.default_home_settings dhs
         WHERE dhs."user" = current_user;
        """)
