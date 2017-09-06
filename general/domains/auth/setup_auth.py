from general.domains.auth.auth_api_schema import AuthApiSchema
from general.domains.auth.auth_schema import AuthSchema


def setup_auth():
    auth_schema = AuthSchema()
    auth_schema.setup()

    auth_api_schema = AuthApiSchema()
    auth_api_schema.setup()


if __name__ == '__main__':
    setup_auth()
