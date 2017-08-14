#!/bin/bash
# wait-for-postgres.sh

set -e

cmd="$@"

until PGPASSWORD=${DJANGO_DB_PASSWORD} psql -h "${DJANGO_DB_HOST}" -U "${DJANGO_DB_USER}" ${DJANGO_DB_NAME} -c '\l' > /dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
