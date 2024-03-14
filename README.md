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

