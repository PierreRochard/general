from general.domains.admin.admin_api_schema import AdminApiSchema
from general.domains.admin.admin_schema import AdminSchema

if __name__ == '__main__':

    admin_schema = AdminSchema()
    admin_schema.setup()

    admin_api_schema = AdminApiSchema()
    admin_api_schema.setup()
