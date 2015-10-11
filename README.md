ubuntu instructions.

Venv is provided, activate with:
    source venv/bin/activate

If heroku is not installed:
    wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
    heroku login
    
If postgres is not installed:
    sudo apt-get install postgresql
    sudo -u postgres createuser $(whoami)
    
To initialize for local, do:
    echo "DATABASE_URL=postgres:///postgres" > .env
    heroku local:run python manage.py migrate
    heroku local:run python manage.py createsuperuser
    
To clear local database, do:
    heroku pg:reset DATABASE_URL

To run locally, do:
    heroku local
    
To initialize for heroku cloud, do:
    heroku create
    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser
    heroku ps:restart
    