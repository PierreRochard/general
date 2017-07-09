from .authenticate_user_email import create_authenticate_user_email_function
from .check_if_role_exists import create_check_if_role_exists_function
from .encrypt_password import create_encrypt_password_function


def create_auth_functions():
    create_authenticate_user_email_function()
    create_check_if_role_exists_function()
    create_encrypt_password_function()
