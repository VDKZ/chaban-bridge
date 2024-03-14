# Chaban bridge

## Start the App

```bash
# Create basic `.env` file:
cp .env.example .env
# Build the containers
docker-compose build --build-arg RUNAS_UID=$(id -u)
# Start app
docker-compose up
```

## Pre commit hook

```bash
pre-commit install
```

## Urls

| Name    | URL                                       |
|---------|-------------------------------------------|
| app     | `http://0.0.0.0:8000/`                    |
| admin   | `http://0.0.0.0:8000/admin/`              |
| api     | `http://0.0.0.0:8000/api/v1/`             |
| swagger | `http://0.0.0.0:8000/api/swagger/`        |


## Running Django commands

```bash
docker-compose run chaban_bridge bash -c "./chaban_bridge/manage.py makemigrations --settings=chaban_bridge.settings.development"
docker-compose run chaban_bridge bash -c "./chaban_bridge/manage.py migrate --settings=chaban_bridge.settings.development"
```

or with run.sh

```bash
# ./run.sh [django_command] [?settings_file]
./run.sh migrate
./run.sh makemigration development
./run.sh "test jobs" test
```