from models import TableColumnSettings

from postgrest_boilerplate.models.util import session_scope


def insert_table_column_settings(user):
    with session_scope() as session:
        for table_name, column_name in session.execute('SELECT table_name, column_name FROM admin.columns'):
            new_record_data = {
                'user': user,
                'table_name': table_name,
                'column_name': column_name,
                'custom_name': column_name.replace('_', ' ').title(),
                'is_filterable': False
            }
            new_record = TableColumnSettings(**new_record_data)
            session.add(new_record)


if __name__ == '__main__':
    insert_table_column_settings('anon')
