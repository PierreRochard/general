The stack

SQLAlchemy

Alembic

PostgreSQL (with barman and repmgr)

Pgbouncer

PostgREST

Nginx

Angular

PrimeNG


<pre>
export PYTHONPATH=$(pwd)
</pre>

<pre>
alembic revision --autogenerate -m "Add users table"
</pre>

git clone https://github.com/michelp/pgjwt

cd pgjwt

make install

### Environment variables

export PGRST_DB_URI="postgres://user:pass@host:5432/dbname"
export PGRST_DB_SCHEMA=""
export PGRST_DB_ANON_ROLE=""
export PGRST_DB_POOL=""
export PGRST_SERVER_HOST=""
export PGRST_SERVER_PORT=""
export PGRST_SERVER_PROXY_URL=""
export PGRST_JWT_SECRET=""
export PGRST_SECRET_IS_BASE64=""
export PGRST_MAX_ROWS=""
export PGRST_PRE_REQUEST=""
