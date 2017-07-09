from postgrest_boilerplate.models import TableColumnSettings, Users, \
    session_scope


def insert_table_column_settings(user):
    with session_scope() as session:
        columns = session.execute('SELECT table_name, column_name FROM admin.columns')
    for table_name, column_name in columns:
        new_record_data = {
            'user': user,
            'table_name': table_name,
            'column_name': column_name,
            'custom_name': column_name.replace('_', ' ').title(),
            'is_filterable': False
        }
        new_record = TableColumnSettings(**new_record_data)
        with session_scope() as session:
            session.add(new_record)


if __name__ == '__main__':
    with session_scope() as session:
        roles = session.query(Users.role).all()
        roles = [r[0] for r in roles]
    roles.append('anon')
    for role in roles:
        insert_table_column_settings(role)
