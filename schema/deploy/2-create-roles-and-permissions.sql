-- Deploy wild-db:2-create-roles-and-permissions to pg
-- requires: 1-create-schema-wild

BEGIN;

-- XXX Add DDLs here.

DO $$
BEGIN

    -- Revoke permissions inherited from "PUBLIC" role
    REVOKE ALL ON SCHEMA public FROM PUBLIC;
    EXECUTE FORMAT(
        'REVOKE ALL ON DATABASE %I FROM PUBLIC',
        current_database()
    );

    -- Create "readonly" role
    CREATE ROLE readonly;

    EXECUTE FORMAT(
        'GRANT CONNECT ON DATABASE %I TO readonly',
        current_database()
    );

    GRANT USAGE ON SCHEMA wild
    TO readonly;

    GRANT SELECT ON ALL TABLES IN SCHEMA wild
    TO readonly;

    ALTER DEFAULT PRIVILEGES IN SCHEMA wild
    GRANT SELECT ON TABLES
    TO readonly;


    -- Create "readwrite" role
    CREATE ROLE readwrite;

    EXECUTE FORMAT(
        'GRANT CONNECT ON DATABASE %I TO readwrite',
        current_database()
    );

    GRANT USAGE ON SCHEMA wild
    TO readwrite;

    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA wild
    TO readwrite;

    ALTER DEFAULT PRIVILEGES IN SCHEMA wild
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES
    TO readwrite;

    ALTER DEFAULT PRIVILEGES IN SCHEMA wild
    GRANT USAGE ON SEQUENCES
    TO readwrite;

END $$;

COMMIT;
