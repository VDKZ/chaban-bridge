#!/bin/bash

python manage.py migrate --settings=chaban_bridge.settings.development
echo "Create Superuser"
python manage.py createsu --settings=chaban_bridge.settings.development --force-reset-password
echo "Run App"
exec python manage.py runserver 0.0.0.0:8000 --settings=chaban_bridge.settings.development
