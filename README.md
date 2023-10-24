# SQL Alchemy POC

#### Requirements

- Make
- Python 3.11
- Docker
- Docker Compose
- Pip
- Other requirements:
    - requirements.txt
    - requirements-dev.txt (development dependencies)

#### Installing dev environment requirements:

```shell
make install-dev
```

#### Linting and formatting code:

```shell
make lint
make format
```

#### Build application:

```shell
make build
```

#### Run application:

```shell
make up
```

#### Build and then run application
```shell
make build-up
```

#### Stop application

```shell
make down
```

### Check application logs:

```shell
make logs
```

## Notes

The project consists in a extremely simple CRUD to know more about SQL Alchemy.

A Postman collection can be found in `api_collection` folder

There are duplicated endpoints for creating, updating, and deleting endpoints. All the endpoints that start with `/orm` consist of the SQL Alchemy ORM approach. The other ones consist of the core approach.
