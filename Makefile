PYTHON=python3
MANAGE=.venv/bin/python app/manage.py
ACTIVATE=. .venv/bin/activate;
BLACK_ARGS=--exclude="migrations|data|lib|bin|var|.venv" .

# Django Configuration
PORT = 8000

virtualenv:
	@echo "-> Making Virtual Environment"
	@${PYTHON} -m venv .venv

install: virtualenv
	@echo "-> Installing Dependencies"
	@${ACTIVATE} pip3 install --upgrade pip
	@${ACTIVATE} pip3 install -r app/requirements.txt

migrate:
	${MANAGE} makemigrations
	@echo "-> Apply database migrations"
	${MANAGE} migrate

run_local:
	${MANAGE} runserver ${PORT}

run_docker:
	docker-compose up --build

flush:
	@echo "-> Flushing Database"
	${MANAGE} flush

format:
	@echo "-> Run isort imports validation"
	@${ACTIVATE} isort .
	@echo "-> Run black validation"
	@${ACTIVATE} black ${BLACK_ARGS}

test: format
	@${MANAGE} test

superuser:
	@${MANAGE} createsuperuser --no-input

db_image:
	@${MANAGE} graph_models -a -g -o imgs/models.png