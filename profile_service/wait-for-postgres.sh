# wait-for-postgres.sh

#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

# Указываем пароль для подключения к PostgreSQL
export PGPASSWORD=$POSTGRES_PASSWORD

until psql -h "$host" -U "postgres" -d "SOCIAL_NETWORK" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd