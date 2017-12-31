from general.database.session_scope import session_scope


def create_menubar_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.menubar CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin.menubar AS
         SELECT u.role AS "user",
                s.id,
                s.submenu_name AS "label",
                s.icon,
                NULL as "routerLink",
                s.order_index,
                si."items" as "items"
         FROM admin.submenus s
         LEFT JOIN auth.users u 
          ON u.id = s.user_id
         LEFT OUTER JOIN (
            SELECT
              si.user,
              si.submenu_id,
              array_to_json(array_agg(row_to_json(si)))::JSONB as "items"
              FROM  admin.submenu_items si
              GROUP BY si.submenu_id, si.user
         ) si
         ON s.id = si.submenu_id AND si.user = u.role
         WHERE s.is_visible
          AND u.role != 'anon'
         UNION
         SELECT 
                dts.user,
                dts.id,
                dts.custom_name AS "label",
                dts.icon, 
                ARRAY['/', dts.schema_name, dts.table_name] AS "routerLink",
                dts.order_index,
                NULL as "items"
         FROM admin.default_datatable_settings dts
         WHERE dts.submenu_id IS NULL AND dts.is_visible
          AND dts."user" != 'anon'
         UNION
         SELECT 
                dfs.user,
                dfs.id,
                dfs.custom_name AS "label",
                dfs.icon,
                ARRAY['/', dfs.schema_name, 'rpc', dfs.form_name] AS "routerLink",
                dfs.order_index,
                NULL as "items"
         FROM admin.default_form_settings dfs
         WHERE dfs.submenu_id IS NULL AND dfs.is_visible
            AND ((dfs.user != 'anon' AND dfs.form_name != 'login')
             OR (dfs.user = 'anon' AND dfs.form_name  != 'logout'))
        
         ORDER BY "user" ASC, order_index ASC NULLS LAST, "label" ASC NULLS LAST;
        """)


if __name__ == '__main__':
    create_menubar_view()
