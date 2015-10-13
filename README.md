Artistally app instructions.

Venv is provided, activate with:
    source venv/bin/activate

If heroku is not installed:
    wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
    heroku login
    
If postgres is not installed:
    sudo apt-get install postgresql
    sudo -u postgres createuser $(whoami)
    
To initialize for local, first create a file .env containing:
    DATABASE_URL = postgres:///postgres
    SECRET_KEY = YOUR_RANDOM_KEY_GOES_HERE
( use this website to generate a secret key: miniwebtool.com/django-secret-key-generator )
Then do:
    heroku local:run python manage.py migrate
    heroku local:run python manage.py createsuperuser
    
To clear local database, do:
    heroku pg:reset DATABASE_URL

To run locally, do:
    heroku local
    
To initialize for heroku cloud, do:
    heroku create
    heroku config:set SECRET_KEY='YOUR_RANDOM_KEY_GOES_HERE'
( again, use this website to generate a secret key: miniwebtool.com/django-secret-key-generator )
( put it in single quotes or bash will complain )
    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser
    heroku ps:restart
    