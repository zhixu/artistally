# Artistally app instructions

## Prerequisites.

0. Be inside the top-level directory of the project.

1. Create and prepare a virtual environment.
    ```vim
    sudo apt-get install python3-venv
    pyvenv venv_
    source venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    ```
2. If heroku is not installed:
    ```vim
    wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
    heroku login
    ```

Virtualenv must be reactivated every time you close and reopen the terminal.

## Preparing the local environment.
1. If postgres is not installed:
    ```vim
    sudo apt-get install postgresql python-psycopg2 libpq-dev
    sudo -u postgres createuser $(whoami)
    ```
2. Environment variables must be specified. Create a file .env containing:
    ```vim
    DEBUG = True
    DATABASE_URL = postgres:///postgres
    SECRET_KEY =
    EMAIL_USE_TLS =
    EMAIL_HOST =
    EMAIL_PORT =
    EMAIL_HOST_USER =
    EMAIL_HOST_PASSWORD =
    ```
3. Fill in the blank fields:_

    <a href="miniwebtool.com/django-secret-key-generator">Use this website to generate a secret key</a>

    The email settings will depend on your preferred SMTP server.

    For example, Gmail uses EMAIL_USE_TLS = True, EMAIL_HOST = smtp.gmail.com, and EMAIL_PORT = 587.

    EMAIL_HOST_USER and EMAIL_HOST_PASSWORD should be your username and password for the SMTP server.

5. Prepare the Django project for first run:
    ```vim
    heroku local:run python manage.py migrate
    heroku local:run python manage.py createsuperuser
    heroku local:run python manage.py collectstatic
    ```

    The last command is optional if you set DEBUG to True.

## Updating Database
Changed the model? You need to update it with the database.

1. Create and apply the migrations:
    ```vim
    heroku local:run python manage.py makemigrations
    heroku local:run python manage.py migrate
    ```

## Running locally.
1. If you have added new files to /aa_app/static since the last time you ran this command, re-run:
    ```vim
    heroku local:run python manage.py collectstatic
    ```

    Do NOT put files yourself into /staticfiles! They will get overwritten!

    ( this is optional if you set DEBUG to True )

2. Start the server:
    ```vim
    heroku local
    ```

## Clearing the local database.
1. Drop and recreate the database:
    ```vim
    sudo -u postgres dropdb postgres
    sudo -u postgres createdb postgres
    ```

## Preparing to run on heroku.
1. Create the heroku app:
    ```vim
    heroku create
    ```

2. Set environment variables in a similar way as to the local .env file:
    ```vim
    heroku config:set DEBUG=False
    heroku config:set SECRET_KEY='YOUR_RANDOM_KEY_GOES_HERE'
    ...
    heroku config:set EMAIL_HOST_PASSWORD='PASSWORD_GOES_HERE'
    ```
    ( if your strings contain strange characters, put it in quotes or bash will complain )
    
3. Push to heroku:
    ```vim
    git push heroku master
    ```
4. Prepare the django project for first run:
    ```vim
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser
    heroku ps:restart
    ```

## Created migrations locally? You need to apply them on heroku as well.
1. (Assuming you committed and pushed it to Heroku) Apply the migrations:
    ```vim
    heroku run python manage.py migrate
    ```

## Clearing the heroku database.
1. Run this command (yes, exactly as is, don't fill in DATABASE_URL)
    ```vim
    heroku pg:reset DATABASE_URL
    ```
