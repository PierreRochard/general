from models import get_session
from models.admin import Messages

session = get_session()

for i in range(0, 50):
    new_message = Messages(to_user='you', subject='test')
    session.add(new_message)
    session.commit()
