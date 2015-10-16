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
    DEBUG = True
    DATABASE_URL = postgres:///postgres
    SECRET_KEY = YOUR_RANDOM_KEY_GOES_HERE
( use this website to generate a secret key: miniwebtool.com/django-secret-key-generator )
Then do:
    heroku local:run python manage.py migrate
    heroku local:run python manage.py createsuperuser
    heroku local:run python manage.py collectstatic
    
If you have added new files to /aa_app/static, re-run:
    heroku local:run python manage.py collectstatic
( do NOT put files yourself into /staticfiles! they will get overwritten! )

To run locally, do:
    heroku local
    
To clear local database, do:
    sudo -u postgres psql dropdb postgres
    sudo -u postgres psql createdb postgres
    
To initialize for heroku cloud, do:
    heroku create
    heroku config:set DEBUG=False
    heroku config:set SECRET_KEY='YOUR_RANDOM_KEY_GOES_HERE'
( again, use this website to generate a secret key: miniwebtool.com/django-secret-key-generator )
( put it in single quotes or bash will complain )
    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser
    heroku ps:restart
    
To clear heroku cloud database, do:
    heroku pg:reset DATABASE_URL
