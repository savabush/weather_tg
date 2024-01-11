#!/bin/bash

# Function to check if a port is open
check_port() {
    local host=$1
    local port=$2
    while ! nc -z "$host" "$port"; do
        echo "Port $port is not open on $host. Retrying in 1 second..."
        sleep 1
    done
    echo "Port $port is open on $host."
}

# Check if PostgreSQL port is open
echo "Checking if PostgreSQL port is open..."
check_port "db" 5432

# Check if Redis port is open
echo "Checking if Redis port is open..."
check_port "redis" 6379

# Start the Django app with Uvicorn
echo "Starting the Django app with Uvicorn..."

python manage.py collectstatic --noinput

python manage.py migrate

uvicorn weather_app.asgi:application --host 0.0.0.0 --port 8000 --workers 4
