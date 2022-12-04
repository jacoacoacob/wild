-- Verify fmc-db:1-create-schema-fmc on pg

BEGIN;

-- XXX Add verifications here.

SELECT 1 / COUNT(*) FROM information_schema.schemata WHERE schema_name = 'fmc';

ROLLBACK;
