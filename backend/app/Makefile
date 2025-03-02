args = $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

run:
	fastapi dev main.py

poetry-check:
	poetry check

ruff:
	ruff format .
	ruff check --fix .
	ruff check .

mypy:
	mypy .

lint: poetry-check ruff mypy

current:
	alembic current

history:
	alembic history

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade $(args)

migrations:
	alembic revision --autogenerate -m "$(args)"

%:
	@:
