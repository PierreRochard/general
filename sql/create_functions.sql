CREATE OR REPLACE FUNCTION table_notify() RETURNS trigger AS $$
DECLARE
  id UUID;
  payload text;
  json_record JSON;
  payload_size INT;
BEGIN
  IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
    id = NEW.id;
    json_record = row_to_json(NEW);

--   Creates a DIFF from the OLD row to NEW row on updates, and create a change feed
--   ELSEIF  TG_OP = 'UPDATE' THEN
--     id = NEW.id;
--     json_record = jsonb_diff_val(row_to_json(NEW)::JSONB, row_to_json(OLD)::JSONB);

  ELSE
    id = OLD.id;
    json_record = row_to_json(OLD);
  END IF;
  payload = json_build_object('table_name', TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME, 'id', id, 'type', TG_OP, 'row', json_record)::text;
  payload_size = octet_length(payload);
  IF payload_size >= 8000 THEN
    payload = json_build_object('table_name', TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME, 'id', id, 'type', TG_OP)::text;
  END IF;
  PERFORM pg_notify('messages_table_update', payload);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION jsonb_diff_val(val1 JSONB,val2 JSONB)
RETURNS JSONB AS $$
DECLARE
  result JSONB;
  v RECORD;
BEGIN
   result = val1;
   FOR v IN SELECT * FROM jsonb_each(val2) LOOP
     IF result @> jsonb_build_object(v.key,v.value)
        THEN result = result - v.key;
     ELSIF result ? v.key THEN CONTINUE;
     ELSE
        result = result || jsonb_build_object(v.key,'null');
     END IF;
   END LOOP;
   RETURN result;
END;
$$ LANGUAGE plpgsql;
