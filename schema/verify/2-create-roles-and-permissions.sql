-- Verify wild-db:2-create-roles-and-permissions on pg

BEGIN;

-- XXX Add verifications here.

CREATE TABLE public.out_of_bounds (word TEXT);

INSERT INTO public.out_of_bounds (word)
VALUES ('No way, bud');

CREATE TABLE wild.game_on (
    id SERIAL PRIMARY KEY,
    word TEXT
);

INSERT INTO wild.game_on (word)
VALUES ('Lets go!');

DO $$
BEGIN
    -- Test "readonly" privileges
    SET ROLE readonly;

    BEGIN
        -- if the SELECT statement doesn't raise an "insufficient_privilege" exception,
        -- raise an exception that will cause this "verify" script transaction to rollback
        SELECT * FROM public.game_on;
        RAISE EXCEPTION 'Should not be able to select from tables in schema "public"';
        -- we expect an "insufficient_privilege" exception, when we get it, do nothing
        -- and move on to the next test
        EXCEPTION WHEN insufficient_privilege THEN
    END;

    BEGIN
        INSERT INTO public.game_on VALUES ('icantdothis');
        RAISE EXCEPTION 'Should not be able to insert into tables in schema "public"';
        EXCEPTION WHEN insufficient_privilege THEN
    END;

    BEGIN
        CREATE TABLE wild.cani (dothis boolean);
        RAISE EXCEPTION 'Should not be able to create tables in schema "wild"';
        EXCEPTION WHEN insufficient_privilege THEN
    END;

    BEGIN
        DROP TABLE wild.game_on;
        RAISE EXCEPTION 'Role "readonly" Should not be able to drop tables in schema "wild"';
        EXCEPTION WHEN insufficient_privilege THEN
    END;

    ASSERT (SELECT COUNT(*) FROM wild.game_on) = 1;



    -- Test "readwrite" privileges
    SET ROLE readwrite;

    BEGIN
      INSERT INTO public.out_of_bounds VALUES ('can i do this');
      RAISE EXCEPTION 'Role "readwrite" should not be able to insert into tables in schema "public"';
      EXCEPTION WHEN insufficient_privilege THEN
    END;

    BEGIN
      CREATE TABLE public.candothis (yes BOOLEAN);
      RAISE EXCEPTION 'Role "readwrite" should not be able to create tables in schema "public"';
      EXCEPTION WHEN insufficient_privilege THEN
    END;

    BEGIN
      CREATE TABLE wild.candothis (yes BOOLEAN);
      RAISE EXCEPTION 'Role "readwrite" should not be able to create tables in schema "wild"';
      EXCEPTION WHEN insufficient_privilege THEN
    END;

    INSERT INTO wild.game_on (word) VALUES ('i can do this');

    ASSERT (SELECT COUNT(*) FROM wild.game_on) = 2;
    ASSERT (SELECT word FROM wild.game_on WHERE id = 2) = 'i can do this';

    UPDATE wild.game_on SET word = 'now it is this' WHERE id = 2;

    ASSERT (SELECT word FROM wild.game_on WHERE id = 2) = 'now it is this';

    DELETE FROM wild.game_on WHERE id = 2;

    ASSERT (SELECT COUNT(*) FROM wild.game_on) = 1;

END $$;

ROLLBACK;
