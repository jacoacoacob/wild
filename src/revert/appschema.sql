-- Revert fmc-db:appschema from pg

BEGIN;

-- XXX Add DDLs here.

DROP SCHEMA fmc;

COMMIT;
