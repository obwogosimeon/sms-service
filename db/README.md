# Farmer Database Docker Mock #

Use this repository to set up a docker container that mocks the Farmer Database. 
It sets up the a Postgres container and creates the users and schemas for all of our services.

## Usage

Usually, this repository is used as submodule from other repositories. If you want to start 
the database individually, follow these steps:

Copy the .env file and change the variable `SERVICE_PREFIX`:
```
cp .env.example .env
```

Spin up the container:
```
docker-compose up
```

To delete the container:
```
docker-compose down -v
```
