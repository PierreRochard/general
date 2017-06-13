from models.api import Messages
from models.util import get_session


def insert_messages():
    session = get_session()
    for i in range(0, 50):
        new_message = Messages(user='you', subject='test')
        session.add(new_message)
        session.commit()


if __name__ == '__main__':
    insert_messages()
