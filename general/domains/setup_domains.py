from general.domains.admin.setup_admin import setup_admin
from general.domains.auth.setup_auth import setup_auth


def setup_domains():
    setup_admin()
    setup_auth()

if __name__ == '__main__':
    setup_domains()
