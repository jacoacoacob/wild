-- Revert wild-db:2-create-roles-and-permissions from pg

BEGIN;

-- XXX Add DDLs here.

DO $$
BEGIN
    -- Give back privileges inherited from "PUBLIC" role
    GRANT ALL ON SCHEMA public TO PUBLIC;
    EXECUTE FORMAT(
        'GRANT ALL ON DATABASE %I TO PUBLIC',
        current_database()
    );

    -- Revoke "readonly" privileges and drop role
    EXECUTE FORMAT (
        'REVOKE CONNECT ON DATABASE %I FROM readonly',
        current_database()
    );

    REVOKE USAGE ON SCHEMA wild
    FROM readonly;

    REVOKE SELECT ON ALL TABLES IN SCHEMA wild
    FROM readonly;

    ALTER DEFAULT PRIVILEGES IN SCHEMA wild
    REVOKE SELECT ON TABLES
    FROM readonly;

    DROP ROLE readonly;


    -- Revoke "readwrite" privileges and drop role
    EXECUTE FORMAT(
        'REVOKE CONNECT ON DATABASE %I FROM readwrite',
        current_database()
    );

    REVOKE USAGE ON SCHEMA wild
    FROM readwrite;

    REVOKE SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA wild
    FROM readwrite;

    ALTER DEFAULT PRIVILEGES IN SCHEMA wild
    REVOKE SELECT, INSERT, UPDATE, DELETE ON TABLES
    FROM readwrite;

    ALTER DEFAULT PRIVILEGES IN SCHEMA wild
    REVOKE USAGE ON SEQUENCES
    FROM readwrite;

    DROP ROLE readwrite;

END $$;

COMMIT;
