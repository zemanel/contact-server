.PHONY: deps sync-deps compile-deps

deps: sync-deps
	@echo Updating dependencies

sync-deps: compile-deps
	pip-sync requirements/development.txt requirements/test.txt

compile-deps:
	pip-compile --verbose -o requirements/production.txt src/requirements/production.in
	pip-compile --verbose -o requirements/development.txt src/requirements/production.in src/requirements/development.in
	pip-compile --verbose -o requirements/test.txt src/requirements/production.in src/requirements/test.in

build:
	docker-compose build

migrate: build
	docker-compose run --rm api-development python src/manage.py migrate

run: build migrate
	docker-compose up

test: build
	docker-compose run --rm api-test pytest --verbose

lint:
	cd src && pre-commit run --all-files
