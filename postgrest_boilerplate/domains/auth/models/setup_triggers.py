from .users import create_triggers_on_users, create_constraint_triggers_on_users


def create_auth_table_triggers():
    create_triggers_on_users()
    create_constraint_triggers_on_users()
