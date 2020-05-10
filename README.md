# Fyyur

[![CircleCI](https://circleci.com/gh/MaxBoykoII/fyyur-tdd.svg?style=svg)](https://circleci.com/gh/MaxBoykoII/fyyur-tdd)

## Introduction

(Fyyur)[https://fyyur-dev.herokuapp.com/] is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Development Setup (without Docker)

1.  Initialize and activate a virtualenv:
	```
    $ cd YOUR_PROJECT_DIRECTORY_PATH/
    $ virtualenv --no-site-packages env
    $ source env/bin/activate
    ```
2. Install the dependencies:
   ```
   $ pip install -r requirements.txt
   ```
3. Configure Environment variables:
   ```
   $ export FLASK_ENV=development
   $ export APP_SETTINGS=project.config.DevelopmentConfig
   $ export DATABASE_URL = <YOUR LOCAL DATABASE URL> # database used by app
   $ export DATABASE_TEST_URL = <YOUR LOCAL TEST DATABASE URL> # database used by integration tests
   ```

4. Run development server:
   ```
   $ python manage.py recreate_db # reset db
   $ python manage.py seed_db # seed db
   $ python manage.py run -h 0.0.0.0
   ```
5. Navigate to Home page [http://localhost:5000](http://localhost:5000)
6.  (Optional) Run tests tests:
    ```
    $ python -m pytest "project/tests" -p no:warnings
    ```

## Development Setup (With Docker)

1. Run container:
   ```
   $ cd YOUR_PROJECT_DIRECTORY_PATH/
   $ docker-compose up -d --build
   $ docker-compose exec fyyur python manage.py recreate_db
   $ docker-compose exec fyyur python manage.py seed_db
   ```
2. Navigate to Home page [http://localhost:5001](http://localhost:5001)
3. Run tests and quality checks:
   ```
   $ docker-compose exec fyyur python -m pytest "project/tests" -p no:warnings
   $ docker-compose exec fyyur python -m pytest "project/tests" -p no:warnings --cov="project" # include coverage report
   $ docker-compose exec fyyur flake8 project # lint code
   $ docker-compose exec fyyur black project # format code
   $ docker-compose exec fyyur isort project/**/*.py # sort imports
   ```
4. Connect to database via psql
   ```
   docker-compose exec fyyur-db psql -U postgres
   ```
5. Container cleanup
   ```
   $ docker-compose stop
   $ docker-compose down
   ```