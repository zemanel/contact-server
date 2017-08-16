# About

Django wrapper API for a Google Docs spreadsheet


# Requirements

- Docker + Docker Compose

# Running the project

A Makefile has utilities to run the project:

- Run tests:

        $ make test

- Run development server:

        $ make run

The API endpoints require session authentication. To create a user:

        $ docker-compose run api-development python src/manage.py createsuperuser

Available endpoints:

- <http://0.0.0.0:8000/api/contacts/> : contact list.
 If the `image_height` or `image_height` HTTP parameters are passed,
  images will be resized and uploaded to media storage.

- <http://0.0.0.0:8000/account/login/> : User login


