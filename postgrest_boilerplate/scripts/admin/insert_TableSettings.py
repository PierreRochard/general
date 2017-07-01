from models import Submenus, TableSettings

from postgrest_boilerplate.models.util import session_scope

custom_name_mappings = {
    'form_field_settings':   'Form Fields',
    'form_settings':         'Forms',
    'table_column_settings': 'Table Columns',
    'table_settings':        'Tables',
}
system_table_names = [
    'datatable',
    'datatable_columns',
    'items',
    'menubar'
]


def insert_table_settings(user):
    with session_scope() as session:
        for table_name, in session.execute(
                'SELECT table_name FROM admin.tables'):
            submenu_id = None

            if table_name.endswith('settings'):
                submenu_name = 'Settings'
                submenu_id = (session.query(Submenus.id)
                              .filter(Submenus.submenu_name == submenu_name)
                              .filter(Submenus.user == user)
                              .scalar())

            if table_name in system_table_names:
                is_visible = False
            else:
                is_visible = True

            custom_name = custom_name_mappings.get(table_name, None)
            if custom_name is None:
                custom_name = table_name.replace('_', ' ').title()

            new_record_data = {
                'user':        user,
                'table_name':  table_name,
                'custom_name': custom_name,
                'icon':        'fa-table',
                'submenu_id':  str(submenu_id) if submenu_id else None,
                'is_visible':  is_visible,
                'order_index': 1,
            }
            new_record = TableSettings(**new_record_data)
            session.add(new_record)


if __name__ == '__main__':
    insert_table_settings('anon')
