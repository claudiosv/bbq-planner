#!/bin/sh

python manage.py makemigrations
until python manage.py migrate; do
  sleep 2
  echo "Retry!";
done
python manage.py shell < init_admin.py

python manage.py makemigrations bbqplanner
python manage.py migrate bbqplanner
echo "Django is ready.";

exec "$@"
