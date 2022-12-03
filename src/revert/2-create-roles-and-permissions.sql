-- Revert fmc-db:2-create-roles-and-permissions from pg

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

    REVOKE USAGE ON SCHEMA fmc
    FROM readonly;

    REVOKE SELECT ON ALL TABLES IN SCHEMA fmc
    FROM readonly;

    ALTER DEFAULT PRIVILEGES IN SCHEMA fmc
    REVOKE SELECT ON TABLES
    FROM readonly;

    DROP ROLE readonly;


    -- Revoke "readwrite" privileges and drop role
    EXECUTE FORMAT(
        'REVOKE CONNECT ON DATABASE %I FROM readwrite',
        current_database()
    );

    REVOKE USAGE ON SCHEMA fmc
    FROM readwrite;

    REVOKE SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA fmc
    FROM readwrite;

    ALTER DEFAULT PRIVILEGES IN SCHEMA fmc
    REVOKE SELECT, INSERT, UPDATE, DELETE ON TABLES
    FROM readwrite;

    ALTER DEFAULT PRIVILEGES IN SCHEMA fmc
    REVOKE USAGE ON SEQUENCES
    FROM readwrite;

    DROP ROLE readwrite;

END $$;

COMMIT;
