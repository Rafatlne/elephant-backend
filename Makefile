################################################################################
# Docker compose commands ######################################################

start:
	docker compose up -d --remove-orphans
stop:
	docker compose down
restart:
	docker compose down
	docker compose up -d --remove-orphans
build:
	docker compose build
rebuild:
	docker compose down
	docker compose build
	docker compose up -d --remove-orphans
ps:
	docker compose ps
logs:
	docker compose logs -f
