Artistally app instructions

Prerequisites.
0. Be inside the top-level directory of the project.
1. Create and prepare a virtual environment.
    sudo apt-get install python3-venv
    pyvenv venv
    source venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
2. If heroku is not installed:
    wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
    heroku login

Virtualenv must be reactivated every time you close and reopen the terminal.

Preparing the local environment.
1. If postgres is not installed:
    sudo apt-get install postgresql
    sudo -u postgres createuser $(whoami)
2. Environment variables must be specified. Create a file .env containing:
    DEBUG = True
    DATABASE_URL = postgres:///postgres
    SECRET_KEY = 
    EMAIL_USE_TLS = 
    EMAIL_HOST = 
    EMAIL_PORT = 
    EMAIL_HOST_USER = 
    EMAIL_HOST_PASSWORD = 
3. Fill in the blank fields:
    Use this website to generate a secret key: miniwebtool.com/django-secret-key-generator
    The email settings will depend on your preferred SMTP server.
    For example, Gmail uses EMAIL_USE_TLS = True, EMAIL_HOST = smtp.gmail.com, and EMAIL_PORT = 587.
    EMAIL_HOST_USER and EMAIL_HOST_PASSWORD should be your username and password for the SMTP server.
5. Prepare the Django project for first run:
    heroku local:run python manage.py migrate
    heroku local:run python manage.py createsuperuser
    heroku local:run python manage.py collectstatic
    ( this last command is optional if you set DEBUG to True )
    
Changed the model? You need to update it with the database.
1. Create and apply the migrations:
    heroku local:run python manage.py makemigrations
    heroku local:run python manage.py migrate
    
Running locally.
1. If you have added new files to /aa_app/static since the last time you ran this command, re-run:
    heroku local:run python manage.py collectstatic
    ( do NOT put files yourself into /staticfiles! they will get overwritten! )
    ( this is optional if you set DEBUG to True )
2. Start the server:
    heroku local
    
Clearing the local database.
1. Drop and recreate the database:
    sudo -u postgres dropdb postgres
    sudo -u postgres createdb postgres
    
Preparing to run on heroku.
1. Create the heroku app:
    heroku create
2. Set environment variables in a similar way as to the local .env file:
    heroku config:set DEBUG=False
    heroku config:set SECRET_KEY='YOUR_RANDOM_KEY_GOES_HERE'
    ...
    heroku config:set EMAIL_HOST_PASSWORD='PASSWORD_GOES_HERE'
    ( if your strings contain strange characters, put it in quotes or bash will complain )
3. Push to heroku:
    git push heroku master
4. Prepare the django project for first run:
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser
    heroku ps:restart
    
Created migrations locally? You need to apply them on heroku as well.
1. (Assuming you committed and pushed it to Heroku) Apply the migrations:
    heroku run python manage.py migrate
    
Clearing the heroku database.
1. Run this command (yes, exactly as is, don't fill in DATABASE_URL)
    heroku pg:reset DATABASE_URL
