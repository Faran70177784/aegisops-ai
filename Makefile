.PHONY: install test lint migrate upgrade downgrade run docker-up docker-down seed

install:
	python -m pip install -r requirements.txt

test:
	python -m pytest tests -v

lint:
	python -m compileall -q backend database tests

migrate:
	alembic upgrade head

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

run:
	uvicorn backend.app.main:app --reload

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

seed:
	python database/seeds/seed_rbac.py
	python database/seeds/seed_permissions.py
	python database/seeds/seed_admin.py
	python database/seeds/seed_rbac_users.py
