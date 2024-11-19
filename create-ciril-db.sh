#!/bin/bash

# Define variables
DB_CONTAINER="dt_eng_test-database-1"
DB_HOST="database"
DB_USER="user_dteng"
DB_PASSWORD="cirilgroupt"
DB_NAME="db_dteng"
SQL_FILE="/opt/airflow/example_schema.sql"

# Check if the SQL file exists
if [[ ! -f "$SQL_FILE" ]]; then
  echo "Error: SQL file '$SQL_FILE' not found!"
  exit 1
fi

# Execute the Docker Compose command
# docker compose run "$DB_CONTAINER" mysql \
#   --host="$DB_HOST" \
#   --user="$DB_USER" \
#   --password="$DB_PASSWORD" \
#   "$DB_NAME" < "$SQL_FILE"
# docker compose run "$DB_CONTAINER" sh -c "mysql --host='$DB_HOST' --user='$DB_USER' --password='$DB_PASSWORD' '$DB_NAME' < '$SQL_FILE'"
# Copy the SQL file to the container (optional step)
docker cp "$SQL_FILE" "$DB_CONTAINER:/tmp/example_schema.sql"

# # Execute the SQL script inside the running container
docker exec -i "$DB_CONTAINER" mysql --host="$DB_HOST" --user="$DB_USER" --password="$DB_PASSWORD" "$DB_NAME" < "$SQL_FILE"
# Check if the command succeeded
if [[ $? -eq 0 ]]; then
  echo "SQL script executed successfully."
else
  echo "Error executing SQL script."
fi
