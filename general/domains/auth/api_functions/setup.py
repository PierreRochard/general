from .login import create_login_api_trigger
from .logout import create_logout_api_trigger


def create_auth_api_functions():
    create_login_api_trigger()
    create_logout_api_trigger()
