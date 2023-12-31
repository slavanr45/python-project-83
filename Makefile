dev:
	poetry run flask --app page_analyzer:app run

dev_debug:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

lint:
	poetry run flake8 .

selfcheck:
	poetry check

check: selfcheck lint

build_all: check
	poetry build

build:
	./build.sh

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

.PHONY: install test lint selfcheck check build
