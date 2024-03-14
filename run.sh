COMMAND=$1

# Shortcuts
if [ $COMMAND = "migrate" ]; then
    echo "SHORTCUT: Running 'migrate' with development settings"
   docker-compose run --rm chaban_bridge bash -c "cd ./chaban_bridge && python manage.py migrate --settings=chaban_bridge.settings.development"
elif [ $COMMAND = "makemigrations" ]; then
    echo "SHORTCUT: Running 'makemigrations' with development settings"
   docker-compose run --rm chaban_bridge bash -c "cd ./chaban_bridge && python manage.py makemigrations --settings=chaban_bridge.settings.development"
elif [ $COMMAND = "test" ]; then
    echo "SHORTCUT: Running 'test' with test settings"
    docker-compose run --rm chaban_bridge bash -c "cd ./chaban_bridge && python manage.py test --settings=chaban_bridge.settings.test"
# Raw command
else
    SETTINGS_FILE=$2
    if [ -z "$SETTINGS_FILE" ]
    then
        SETTINGS_FILE="development"
    fi
    docker-compose run --rm chaban_bridge bash -c "cd ./chaban_bridge && python manage.py $COMMAND --settings=chaban_bridge.settings.$SETTINGS_FILE"
fi
