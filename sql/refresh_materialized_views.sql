REFRESH MATERIALIZED VIEW admin.tables;
REFRESH MATERIALIZED VIEW admin.forms;
REFRESH MATERIALIZED VIEW admin.columns;
GRANT EXECUTE ON FUNCTION api.login(TEXT, TEXT) TO anon;