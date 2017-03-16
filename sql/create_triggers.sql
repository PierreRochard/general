DROP TRIGGER IF EXISTS messages_notify_update ON api.messages;
CREATE TRIGGER messages_notify_update
AFTER UPDATE ON api.messages
FOR EACH ROW EXECUTE PROCEDURE table_notify();

DROP TRIGGER IF EXISTS messages_notify_insert ON api.messages;
CREATE TRIGGER messages_notify_insert
AFTER INSERT ON api.messages
FOR EACH ROW EXECUTE PROCEDURE table_notify();

DROP TRIGGER IF EXISTS messages_notify_delete ON api.messages;
CREATE TRIGGER messages_notify_delete
AFTER DELETE ON api.messages
FOR EACH ROW EXECUTE PROCEDURE table_notify();
