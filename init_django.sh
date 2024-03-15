#!/bin/sh

bash -c "python manage.py makemigrations --noinput"
bash -c "python manage.py migrate"

script="
from django.contrib.auth.models import User;

username = '$DJANGO_USER';
password = '$DJANGO_PASSWORD';
email = '';

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python manage.py shell

bash -c "python manage.py collectstatic --noinput"

#bash -c "gunicorn core.wsgi:application -w 2 --bind :8000 --reload"

bash -c "python manage.py runserver 0.0.0.0:8000"