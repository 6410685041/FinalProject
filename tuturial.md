# Make PostgreSQL on docker

``` terminal
$ docker run --name <name> -p 5432:5432 -e POSTGRES_PASSWORD=<password> -d postgres
```

### if already have containers

``` terminal
$ docker start postgres
```

### for stop docker

``` terminal
$ docker stop postgres
```

# Using docker compose for run multi-container

``` terminal
$ docker-compose up -d
```

# for secret key

create `.env` file in web folder to put secret key 

``` env
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
GOOGLE_CID=
GOOGLE_CSECRETS=
DJANGO_SECRET_KEY=
```

# for postgres container (db)

### for go into db with exec

``` sh
psql -U <username> -d <database_name>
```

### for find all table in database

```sh
select * from pg_catalog.pg_tables where schemaname='public';
```

### if you forget `;` at the end of command, reset code with

```sh
\r
```

### for check each column in table

```sh
\d <column name>;
```

### for check each row in table

```sh
select * from <column name>;
```

# For Website

## if there is problem with `django site`

go to docker `exec in web container` and use this command for make migrations and migrate

```terminal
python script.py -m
```

then refresh web again

## if there is problem with `MultipleObjectsReturned`

look at `social applications` in admin site, make sure that your provider login have already selected **site for using** --> the site for using should be in the left box

