.PHONY: deps sync-deps compile-deps

deps: sync-deps
	@echo Updating dependencies

sync-deps: compile-deps
	pip-sync requirements/development.txt

compile-deps:
	pip-compile --verbose -o requirements/production.txt src/requirements/production.in
	pip-compile --verbose -o requirements/development.txt src/requirements/production.in src/requirements/development.in
	pip-compile --verbose -o requirements/test.txt src/requirements/production.in src/requirements/test.in
