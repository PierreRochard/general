from general.database.session_scope import session_scope


def create_default_home_settings_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_home_settings CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin.default_home_settings AS 
              SELECT coalesce(hs.id, auth.gen_random_uuid()) as id, 
                     u.role as "user",
                     u.id as user_id,
                     
                     coalesce(hs.custom_name, 'General') AS custom_name,
                     coalesce(hs.headline, 'Welcome') as headline,
                     coalesce(hs.icon, 'fa-home') AS icon,
                     coalesce(hs.sub_headline, '') as sub_headline,
                     coalesce(hs.supporting_image, '') as supporting_image
              FROM auth.users u
              LEFT OUTER JOIN admin.home_settings hs
                  ON u.id = hs.user_id
              ORDER BY u.role;
        """)
