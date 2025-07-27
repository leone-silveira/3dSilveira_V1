# Caminho da raiz do projeto
APP_PATH=backend

# Comando principal para rodar o app
run:
	python -m $(APP_PATH).main

# Criar tabelas e popular dados
populate:
	docker exec -it filament_api python -m database.populate

migrate:
	alembic upgrade head
