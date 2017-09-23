from general.database.session_scope import session_scope


def create_items_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.submenu_items CASCADE;
        """)
        session.execute("""
        CREATE OR REPLACE VIEW admin.submenu_items AS 
                   SELECT 
                dts.user,
                dts.id,
                dts.custom_name AS "label",
                dts.icon, 
                ARRAY['/', dts.schema_name, dts.table_name] AS "routerLink",
                dts.order_index,
                NULL as "items",
                dts.submenu_id
         FROM admin.default_datatable_settings dts
         WHERE dts.submenu_id IS NOT NULL
         UNION
         SELECT 
                dfs.user,
                dfs.id,
                dfs.custom_name AS "label",
                dfs.icon,
                ARRAY['/', dfs.schema_name, 'rpc', dfs.form_name] AS "routerLink",
                dfs.order_index,
                NULL as "items",
                dfs.submenu_id
         FROM admin.default_form_settings dfs
         WHERE dfs.submenu_id IS NOT NULL
        
         ORDER BY order_index ASC NULLS LAST, "label" ASC NULLS LAST;
          """)

if __name__ == '__main__':
    create_items_view()
