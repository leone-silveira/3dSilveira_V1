APP_PATH=backend
#TODO : setting up makefile configs
run:
	python -m $(APP_PATH).main

populate:
	docker exec -it filament-api python -m database.populate

migrate:
	alembic upgrade head
