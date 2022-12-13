-- Revert wild-db:1-create-schema-wild from pg

BEGIN;

-- XXX Add DDLs here.

DROP SCHEMA wild;

COMMIT;
