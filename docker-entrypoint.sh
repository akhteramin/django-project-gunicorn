#!/bin/bash
python manage.py collectstatic --noinput  # Collect static files


# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn -c gunicorn.py ipaypos.wsgi \
    "$@"
