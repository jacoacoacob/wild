# DataBot

Progrums to get data from places into places.

## Quick Start

Spin up a postgres docker container
```
$ docker compose up -d database
```

Run the migrations defined in [./schema](./schema/)
```
$ docker compose run --rm sqitch deploy
```

Connect to our database as *postgres* and setup a user for DataBot to connect with
```
$ docker compose exec database psql -U postgres

postgres=# CREATE ROLE data_bot WITH LOGIN PASSWORD 's00prs3crt';
postgres=# GRANT readwrite TO data_bot;
```

Create a .env file in the project root with the following contents
```
DB_USER=data_bot
DB_PASSWORD=s00prs3crt

DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5436/postgres
```

If you haven't already, install python dependancies on your machine
```
$ poetry install
```

Kick off a job to download a bunch of zip archives, extract CSVs from them, transform some data in those CSVs and then copy those CSVs into our postgres database (this will take a while the first time you run it)
```
$ poetry run cli sync-retr --verbose 1
```

Connect to the database and start poking around!
