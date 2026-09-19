#!/bin/bash

set -e
set -u

function create_user_and_database() {
    local database=$1
    local username=$2
    local password=$3

    echo "Creating user '$username' and database '$database'"

    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE USER $username WITH PASSWORD '$password';
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $username;
EOSQL

    echo "User '$username' and database '$database' created successfully"
}


create_user_and_database \
    "$ELT_DATABASE_NAME" \
    "$ELT_DATABASE_USERNAME" \
    "$ELT_DATABASE_PASSWORD"



echo "Creating schemas and tables in $ELT_DATABASE_NAME"

psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$ELT_DATABASE_NAME" <<-EOSQL

    -- Schemas
    CREATE SCHEMA IF NOT EXISTS staging;
    CREATE SCHEMA IF NOT EXISTS core;


    -- Staging table
    CREATE TABLE IF NOT EXISTS staging.videos (
        video_id VARCHAR(50) PRIMARY KEY,
        title TEXT,
        published_at TIMESTAMP,
        duration VARCHAR(20),
        views BIGINT,
        likes BIGINT,
        comments BIGINT
    );


    -- Core table
    CREATE TABLE IF NOT EXISTS core.videos (
        video_id VARCHAR(50) PRIMARY KEY,
        title TEXT,
        published_at TIMESTAMP,
        duration_seconds INTEGER,
        views BIGINT,
        likes BIGINT,
        comments BIGINT
    );


    -- Permissions
    GRANT USAGE, CREATE ON SCHEMA staging TO $ELT_DATABASE_USERNAME;
    GRANT USAGE, CREATE ON SCHEMA core TO $ELT_DATABASE_USERNAME;

    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging
        TO $ELT_DATABASE_USERNAME;

    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA core
        TO $ELT_DATABASE_USERNAME;

    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA staging
        TO $ELT_DATABASE_USERNAME;

    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA core
        TO $ELT_DATABASE_USERNAME;

EOSQL

echo "Schemas and tables created successfully"

echo "All databases, schemas and tables created successfully"