===============================
stealthx
===============================

    Releasing this personal project to the public domain, and become part of my personal portfolio. Thus *all rights are reserved.*


Quickstart
----------

Run the following commands to bootstrap your environment ::

    git clone https://github.com/psdon/stealthx
    cd stealthx
    pip install -r requirements/dev.txt
    cp .env.example .env
    npm install
    npm start  # run the webpack dev server and flask server using concurrently

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration ::

    flask db init
    flask db migrate
    flask db upgrade
    npm start


Deployment
----------

To deploy::

    export FLASK_ENV=production
    export FLASK_DEBUG=0
    export DATABASE_URL="<YOUR DATABASE URL>"
    npm run build   # build assets with webpack
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests/Linter
--------------------

To run all tests, run ::

    flask test

To run the linter, run ::

    flask lint

The ``lint`` command will attempt to fix any linting/style errors in the code. If you only want to know if the code will pass CI and do not wish for the linter to make changes, add the ``--check`` argument.

Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.

If you will deploy your application remotely (e.g on Heroku) you should add the `migrations` folder to version control.
You can do this after ``flask db migrate`` by running the following commands ::

    git add migrations/*
    git commit -m "Add migrations"

Make sure folder `migrations/versions` is not empty.


Docker
------

This app can be run completely using ``Docker`` and ``docker-compose``. Before starting, make sure to create a new copy of ``.env.example`` called ``.env``. You will need to start the development version of the app at least once before running other Docker commands, as starting the dev app bootstraps a necessary file, ``webpack/manifest.json``.

There are three main services:

To run the development version of the app ::

    docker-compose up flask-dev

To run the production version of the app ::

    docker-compose up flask-prod

The list of ``environment:`` variables in the ``docker-compose.yml`` file takes precedence over any variables specified in ``.env``.

To run any commands using the ``Flask CLI`` ::

    docker-compose run --rm manage <<COMMAND>>

Therefore, to initialize a database you would run ::

    docker-compose run --rm manage db init

A docker volume ``node-modules`` is created to store NPM packages and is reused across the dev and prod versions of the application. For the purposes of DB testing with ``sqlite``, the file ``dev.db`` is mounted to all containers. This volume mount should be removed from ``docker-compose.yml`` if a production DB server is used.


Asset Management
----------------

Files placed inside the ``assets`` directory and its subdirectories
(excluding ``js`` and ``css``) will be copied by webpack's
``file-loader`` into the ``static/build`` directory. In production, the plugin
``Flask-Static-Digest`` zips the webpack content and tags them with a MD5 hash.
As a result, you must use the ``static_url_for`` function when including static content,
as it resolves the correct file name, including the MD5 hash.
For example::

    <link rel="shortcut icon" href="{{ "{{" }}static_url_for('static', filename='build/img/favicon.ico') {{ "}}" }}">

If all of your static files are managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they
should cache all your assets forever by including the following line
in ``.env``::

    SEND_FILE_MAX_AGE_DEFAULT=31556926  # one year
