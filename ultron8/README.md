# Primary Code

This directory contains the primary code for the API and Automation Executors. The api server is started via `make serve-daemon` and the executor server is started via `make start-executor`.

> Note: Some of the structure of this project is inspired by https://github.com/3lpsy/bountydns

## Folders

### API

The `api` directory contains the FastAPI application instance, the API config, and the Controller methods (routers).

### Migrations

The `migrations` directory container alembic schema code to build out the database.

### Constants

The `constants` directory contains various constants used by components of this application

### Utils

The `utils` directory contains generic utility modules used by this application

### Docs

The `docs` directory contains documentation

### Config

The config directory contains generic configuration classes

### Static

?

### Serialize

?

### Core

The `core` directory contains many different components that are used in both the API and DNS servers. Primarily, it contains different "entity" classes. Entity classes could refer to a response class, a data class, a form class, or repo class related to a data model (the model class is not in this directory). This directory also contains security utilities as well as general utilities/helpers.

As part of the entity classes, a repo class is a helper class that allows for easily building database queries for a model as well as transforming the results to a data class.

### DB

The DB directory contains database models, migrations, factories, queries, and db instances (utility methods).
