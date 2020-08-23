#!/bin/sh

python manage.py flush --no-input
python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --noinput

exec "$@"
