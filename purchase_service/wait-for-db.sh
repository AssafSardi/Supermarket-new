#!/bin/sh
set -e

host="$1"
shift
cmd="$@"

echo "Waiting for Postgres at $host:5432..."

until pg_isready -h "$host" -p 5432; do
  sleep 2
done

echo "Postgres is ready, starting the app..."
exec $cmd
