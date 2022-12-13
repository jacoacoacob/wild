# WILD (WI Landlord Database)

WILD aspires to spotlight legal, temporal, and geographic relationships between residential rental property owners/managers and the properties they control. 
The code in this repository is responsible for two broad tasks:
1. Defining and managing changes to the structure of our [PostgreSQL](https://www.postgresql.org/docs/14/index.html) ("postgres" for short) database that hosts WILD data and makes it queryable.
2. Automating the work of downloading, cleaning, and putting data from various sources into our postgres database.

- [Quick Start](#quick-start)
- [Project structure](#project-structure)
- [Modifying the database schema](#modifying-the-database-schema)
- [Using `data_bot`](#using-data_bot)

## Quick Start

Prerequisites:
- [Python3.10](https://github.com/pyenv/pyenv) (or greater) and [Poetry](https://python-poetry.org/)
- [Docker and Docker Compose](https://docs.docker.com/get-docker/)


From the project root, execute the following commands to setup a postgres database, and download/clean/copy WI Real Estate Transaction Return (RETR) data into it.

1. Spin up a postgres docker container
    ```
    $ docker compose up -d database
    ```

2. Run the migrations defined in [./schema](./schema/)
    ```
    $ docker compose run --rm sqitch deploy
    ```

3. Connect to our database as *postgres* and setup a user for [`data_bot`](#using-data_bot) to connect with
    ```
    $ docker compose exec database psql -U postgres

    postgres=# CREATE ROLE data_bot WITH LOGIN PASSWORD 's00prs3crt';
    postgres=# GRANT readwrite TO data_bot;
    ```

4. Create a .env file in the project root with the following contents
    ```
    DB_USER=data_bot
    DB_PASSWORD=s00prs3crt

    DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5436/postgres
    ```

5. If you haven't already, install python dependancies on your machine
    ```
    $ poetry install
    ```

6. Kick off a job to download a bunch of zip archives, extract CSVs from them, transform some data in those CSVs and then copy those CSVs into our postgres database (this will take a while the first time you run it)
    ```
    $ poetry run data_bot sync-retr --verbose 1
    ```

When that's done, you can connect to the database and start poking around!

## Project Structure

```
.
├── data_bot
│   ├── cli.py
│   ├── lib
│   └── retr
├── schema
│   ├── deploy
│   ├── revert
│   ├── verify
│   ├── sqitch.conf
│   └── sqitch.plan
├── .env # optional and nice to have
├── .gitignore
├── README.md
├── docker-compose.yml
├── poetry.lock
└── pyproject.toml
```

## Modifying the database schema

## Using `data_bot`

`data_bot` is a CLI (written with [`click`](https://click.palletsprojects.com/)) that provides commands to get data from places into places. Assuming you've followed the steps 1-5 outlined in the [quick start](#quick-start), refer to the built-in CLI documentation by running:
```
$ poetry run data_bot
```
You'll see output like:
```                                
Usage: data_bot [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  retr  Commands for interacting with Real Estate Transaction Return...
```
