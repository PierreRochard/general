from postgrest_boilerplate.models import FormSettings, session_scope


def insert_form_settings(user):
    with session_scope() as session:
        for form_name, in session.execute('SELECT form_name FROM admin.forms'):
            new_record_data = {
                'user': user,
                'form_name': form_name,
                'custom_name': form_name.replace('_', ' ').title(),
                'icon': 'fa-pencil-square-o',
                'submenu_id': None,
                'order_index': 10,
            }
            new_record = FormSettings(**new_record_data)
            session.add(new_record)



if __name__ == '__main__':
    insert_form_settings('anon')
