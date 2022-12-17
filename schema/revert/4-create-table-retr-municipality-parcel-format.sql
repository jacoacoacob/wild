-- Revert wild-db:4-create-table-retr-municipality-parcel-formats from pg

BEGIN;

-- XXX Add DDLs here.

DROP TABLE wild.retr_municipality_parcel_format;

COMMIT;
