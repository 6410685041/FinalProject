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