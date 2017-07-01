from sqlalchemy.orm import scoped_session

from models.api import Messages


def insert_messages():
    with scoped_session() as session:
        for i in range(0, 50):
            new_message = Messages(user='you', subject='test')
            session.add(new_message)


if __name__ == '__main__':
    insert_messages()
