#!/bin/sh
echo "db init"
flask db init
echo "db migrate"
flask db migrate
echo "db upgrade"
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - --workers 4 vapehookah:app