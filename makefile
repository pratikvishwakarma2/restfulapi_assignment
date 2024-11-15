.PHONY: run build pinstall pytest format

run:
	@docker compose up

build:
	@docker compose -p fastapi_server up --build

pinstall:
	@pip install -r requirements.txt

pytest:
	@docker exec -it fastapi-user pytest -vs

format:
	black ./src
	isort ./src