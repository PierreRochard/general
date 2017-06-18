from models.util import get_session
from models import TableColumnSettings


def insert_table_column_settings(user):
    session = get_session()
    for table_name, column_name in session.execute('SELECT table_name, column_name FROM admin.columns'):
        new_record_data = {
            'user': user,
            'table_name': table_name,
            'column_name': column_name,
            'custom_name': column_name.replace('_', ' ').title(),
        }
        new_record = TableColumnSettings(**new_record_data)
        session.add(new_record)
        session.commit()


if __name__ == '__main__':
    insert_table_column_settings('anon')
