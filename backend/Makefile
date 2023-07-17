# Refactoring
isort:
	poetry run isort app

black:
	poetry run black app

flake:
	poetry run flake8 app

lint: black isort flake


# Alembic
generate:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

init:
	alembic init -t async migrations


# Arq
arq:
	poetry run arq app.core.scheduler.worker.WorkerSettings