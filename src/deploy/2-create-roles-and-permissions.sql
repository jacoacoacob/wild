-- Deploy fmc-db:2-create-roles-and-permissions to pg
-- requires: 1-create-schema-fmc

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

    GRANT USAGE ON SCHEMA fmc
    TO readonly;

    GRANT SELECT ON ALL TABLES IN SCHEMA fmc
    TO readonly;

    ALTER DEFAULT PRIVILEGES IN SCHEMA fmc
    GRANT SELECT ON TABLES
    TO readonly;


    -- Create "readwrite" role
    CREATE ROLE readwrite;

    EXECUTE FORMAT(
        'GRANT CONNECT ON DATABASE %I TO readwrite',
        current_database()
    );

    GRANT USAGE ON SCHEMA fmc
    TO readwrite;

    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA fmc
    TO readwrite;

    ALTER DEFAULT PRIVILEGES IN SCHEMA fmc
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES
    TO readwrite;

    ALTER DEFAULT PRIVILEGES IN SCHEMA fmc
    GRANT USAGE ON SEQUENCES
    TO readwrite;

END $$;

COMMIT;
