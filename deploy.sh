sudo chmod -R 755 *
git reset --hard HEAD
git pull

#!/bin/bash

NAME="bhancha" # Name of the application
DJANGODIR=/home/anup/bhancha/website # Django project directory
BINDIP=127.0.0.1:8000 # bind gunicorn to this IP address
NUM_WORKERS=9 # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=bhancha.settings # which settings file should Django use
DJANGO_WSGI_MODULE=bhancha.wsgi # WSGI module name
USER=root
GROUP=root
echo "Starting $NAME"

cd $DJANGODIR
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind=$BINDIP \
--log-file=-
