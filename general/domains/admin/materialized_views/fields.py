from general.database.util import session_scope


def create_fields_intermediate_view():
    with session_scope() as session:
        session.execute("""
        DROP VIEW IF EXISTS admin.fields_intermediate CASCADE;
        """)
        session.execute("""
          CREATE OR REPLACE VIEW admin.fields_intermediate AS
            SELECT
              name_sub2.id,
              name_sub2.schema_id,
              name_sub2.form_name,
              name_sub2.name,
              type_sub2.arg_type
            FROM (SELECT (
                     row_number() OVER())::INT id,
                     name_sub1.*
                  FROM
                    (
                      SELECT
                        pg_proc.pronamespace as schema_id,
                        pg_proc.proname as form_name,
                        unnest(pg_proc.proargnames) as name
                      FROM pg_catalog.pg_proc
                      WHERE pg_proc.proargnames IS NOT NULL
                      ORDER BY proname, proargtypes, pronamespace
                    ) name_sub1) name_sub2
            LEFT JOIN
            (SELECT (
                     row_number() OVER())::INT id,
                     type_sub1.arg_type,
                     type_sub1.form_name
            FROM
              (
                SELECT pg_proc.proname as form_name,
                      unnest(pg_proc.proargtypes) as arg_type
                FROM pg_catalog.pg_proc
                WHERE pg_proc.proargnames IS NOT NULL
                ORDER BY proname, proargtypes, pronamespace
              ) type_sub1) type_sub2
              ON type_sub2.id = name_sub2.id
                AND type_sub2.form_name = name_sub2.form_name;
        """)


def create_fields_materialized_view():
    with session_scope() as session:
        session.execute("""
            DROP MATERIALIZED VIEW IF EXISTS admin.fields CASCADE;
        """)
        session.execute("""
            CREATE MATERIALIZED VIEW admin.fields AS
                SELECT 
                    pg_namespace.nspname as schema_name,
                    fi.form_name,
                    fi.name,
                    pg_type.typname as field_type
                FROM admin.fields_intermediate fi
                LEFT JOIN pg_namespace ON pg_namespace.OID = fi.schema_id
                LEFT JOIN pg_type on pg_type.oid = fi.arg_type
                WHERE pg_namespace.nspname = 'api';
        """)

if __name__ == '__main__':
    create_fields_materialized_view()

# SELECT (row_number() OVER())::INT id, sub1.* FROM
# (SELECT pg_proc.proname as form_name,
#                            unnest(pg_proc.proargnames) as name
# FROM pg_catalog.pg_proc) sub1
# ;