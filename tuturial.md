# Make PostgreSQL on docker

``` terminal
$ docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

## if already have containers

``` terminal
$ docker start postgres
```

## for stop docker

``` terminal
$ docker stop postgres
```

# Using docker compose for run multi-container

``` terminal
$ docker-compose up -d
```