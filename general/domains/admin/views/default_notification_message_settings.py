from general.database.session_scope import session_scope


def create_default_notification_message_settings_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.default_notification_message_settings CASCADE;
        """)
        session.execute("""
            CREATE OR REPLACE VIEW admin.default_notification_message_settings AS 
              SELECT u.role as "user",
                     nms.*

              FROM auth.users u
              LEFT JOIN admin.notification_message_settings nms
                  ON nms.user_id = u.id;
        """)
