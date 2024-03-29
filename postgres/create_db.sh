#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER "$POSTGRES_CHABAN_BRIDGE_USER" PASSWORD '$POSTGRES_CHABAN_BRIDGE_PASSWORD';
    CREATE DATABASE "$POSTGRES_CHABAN_BRIDGE_DB";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_CHABAN_BRIDGE_DB" TO "$POSTGRES_CHABAN_BRIDGE_USER";
    ALTER USER "$POSTGRES_CHABAN_BRIDGE_USER" CREATEDB;
EOSQL
