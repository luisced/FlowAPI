#!/bin/bash

# Function to perform initial setup like migrations and superuser creation
initial_setup() {
    # Create migrations if there are changes
    echo "Checking for changes that require migrations..."
    python manage.py makemigrations --dry-run | grep 'No changes detected' || {
        echo "Creating migrations..."
        python manage.py makemigrations djangoapp
        echo "<==================================>"
    }

    # Apply migrations
    echo "Applying migrations..."
    python manage.py migrate
    echo "<==================================>"

    # Create a superuser if it doesn't exist (customize this command as needed)
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput || true  # '|| true' to ignore if the user already exists
    echo "<==================================>"
}

# Function to start Gunicorn with dynamic reload-extra-file options
start_gunicorn() {
    # Generate the reload-extra-file options dynamically
    # extra_files=$(find /app -name "*.html" -o -name "*.py" -printf "--reload-extra-file %p ")

    # Start Gunicorn
    echo "Starting Gunicorn..."
    echo "<==================================>"
    gunicorn djangoproject.wsgi:application -w 2 -b 0.0.0.0:8000 --reload
}

# Run initial setup
initial_setup

