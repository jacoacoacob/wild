-- Revert fmc-db:1-create-schema-fmc from pg

BEGIN;

-- XXX Add DDLs here.

DROP SCHEMA fmc;

COMMIT;
