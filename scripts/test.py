import argparse

from models import get_session
from models.auth import Messages


def insert_records(database, user):
    session = get_session(database, user)
    for i in range(0, 50):
        new_message = Messages(to_user='you', subject='test')
        session.add(new_message)
        session.commit()


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description='Create test records')
    argument_parser.add_argument('-d', help='Database name', dest='database')
    argument_parser.add_argument('-u', help='Database user', dest='user')
    args = argument_parser.parse_args()
    insert_records(args.database, args.user)
